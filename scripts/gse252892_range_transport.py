"""Exact-origin ranged transfer with bounded retries, lineage charges and full MD5 promotion."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import ssl
import threading
import time
import urllib.error
import urllib.request

SETTINGS={'chunk_bytes':32*1024**2,'workers':4,'attempts':3,'socket_seconds':120,'overlap_bytes':1024**2,'backoff_seconds':[2,10]}


class IntegrityError(ValueError):pass
class RetryableError(OSError):
    def __init__(self,message,delay=0):super().__init__(message);self.delay=delay


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):raise IntegrityError('Redirect refused')


def save(path,data):
    path=Path(path);tmp=path.with_name(path.name+'.tmp')
    with tmp.open('w') as f:
        json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)


def digest_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024**2),b''):h.update(b)
    return h.hexdigest()


class Budget:
    def __init__(self,path,cap,prior):
        self.path=Path(path);self.cap=cap;self.prior=prior
        self.observed=0;self.charged=0;self.active={};self.serial=0;self.completed=0
        self.lock=threading.RLock();self.receipts=self.path.parent/'transport-receipts';self.receipts.mkdir()
        self.last=None;self.persist()
    def upper(self):return self.prior+self.charged+sum(r['inflight_max_bytes'] for r in self.active.values())
    def persist(self):
        save(self.path,{'prior_charge_bytes':self.prior,'new_observed_body_bytes':self.observed,
            'actual_body_bytes':self.prior+self.observed,'new_charged_upper_bytes':self.charged,
            'body_upper_bound_bytes':self.upper(),'cap_bytes':self.cap,'request_attempts':self.serial,
            'completed_attempts':self.completed,'active_requests':list(self.active.values()),
            'last_completed':self.last,'receipt_directory':str(self.receipts)})
    def start(self,url,start,end,total,attempt):
        with self.lock:
            if self.upper()>=self.cap:raise IntegrityError('Lineage transfer cap exhausted')
            self.serial+=1;r={'id':self.serial,'url':url,'start':start,'end':end,'total':total,'attempt':attempt,
                'observed_bytes':0,'charged_bytes':0,'uncertain_bytes':0,'inflight_max_bytes':0,'status':'started'}
            self.active[r['id']]=r;self.persist();return r
    def read(self,r,stream,n):
        with self.lock:
            n=min(n,self.cap-self.upper())
            if n<=0:raise IntegrityError('Lineage transfer cap exhausted')
            r['inflight_max_bytes']=n;self.persist()
        try:b=stream.read(n)
        except BaseException:
            with self.lock:
                r['charged_bytes']+=n;r['uncertain_bytes']+=n;self.charged+=n;r['inflight_max_bytes']=0;self.persist()
            raise
        if len(b)>n:raise IntegrityError('Reader exceeded its reserved block')
        with self.lock:
            r['observed_bytes']+=len(b);r['charged_bytes']+=len(b);self.observed+=len(b);self.charged+=len(b)
            r['inflight_max_bytes']=0;self.persist()
        return b
    def finish(self,r,status,error=None):
        with self.lock:
            if r['inflight_max_bytes']:
                n=r['inflight_max_bytes'];self.charged+=n;r['charged_bytes']+=n;r['uncertain_bytes']+=n;r['inflight_max_bytes']=0
            r['status']=status
            if error:r['error']=str(error)
            target=self.receipts/f'{r["id"]:06d}.json'
            if target.exists():raise IntegrityError('Receipt would overwrite evidence')
            save(target,r);del self.active[r['id']];self.completed+=1
            self.last={'id':r['id'],'status':status,'observed_bytes':r['observed_bytes'],'charged_bytes':r['charged_bytes']}
            self.persist()


def blocks(start,total,size):return [(a,min(a+size,total)-1) for a in range(start,total,size)]


def check_headers(resp,url,start,end,total,etag):
    if resp.status!=206 or resp.geturl()!=url:raise IntegrityError('Exact HTTP 206 range response required; no full-file fallback')
    if resp.headers.get('Content-Encoding','identity')!='identity':raise IntegrityError('Unexpected range content encoding')
    wanted=f'bytes {start}-{end}/{total}'
    if resp.headers.get('Content-Range')!=wanted:raise IntegrityError('Content-Range mismatch')
    if resp.headers.get('Content-Length')!=str(end-start+1):raise IntegrityError('Range Content-Length mismatch')
    found=resp.headers.get('ETag')
    if etag is not None and found!=etag:raise IntegrityError('Object validator changed')
    return found if found and found.startswith('"') else None


def one_range(item,start,end,directory,budget,settings,stop,etag=None,opener=None,sleep=time.sleep):
    total=int(item['compressed_bytes']);url=item['url'];directory=Path(directory)
    for attempt in range(1,settings['attempts']+1):
        if stop.is_set():raise IntegrityError('Cancelled after peer failure')
        r=budget.start(url,start,end,total,attempt)
        partial=directory/f'range-{start:012d}-{end:012d}-a{attempt}.partial'
        r['partial_path']=str(partial)
        if partial.exists():budget.finish(r,'failed','Partial exists');raise IntegrityError('No partial overwrite')
        h=hashlib.sha256();error=None
        try:
            headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity','User-Agent':'ela-research/bounded-range'}
            if etag:headers['If-Range']=etag
            req=urllib.request.Request(url,headers=headers)
            op=opener or urllib.request.build_opener(NoRedirect())
            try:resp=op.open(req,timeout=settings['socket_seconds'])
            except urllib.error.HTTPError as exc:
                with exc:
                    # Bound diagnostic error payloads; the consumed prefix is charged.
                    budget.read(r,exc,65536)
                if exc.code in (408,429,500,502,503,504):
                    delay=exc.headers.get('Retry-After','0') if exc.headers else '0'
                    if not delay.isdigit() or int(delay)>120:raise IntegrityError('Retry-After requires separate review')
                    raise RetryableError('Transient HTTP '+str(exc.code),int(delay)) from exc
                raise IntegrityError('Non-retryable HTTP '+str(exc.code)) from exc
            except urllib.error.URLError as exc:
                if isinstance(exc.reason,ssl.SSLCertVerificationError):raise IntegrityError('TLS certificate failure') from exc
                raise RetryableError(str(exc)) from exc
            except (TimeoutError,ConnectionError) as exc:raise RetryableError(str(exc)) from exc
            with resp,partial.open('xb') as out:
                found=check_headers(resp,url,start,end,total,etag);r['etag']=resp.headers.get('ETag')
                count=0;expected=end-start+1
                while True:
                    if stop.is_set():raise IntegrityError('Cancelled after peer failure')
                    try:b=budget.read(r,resp,min(1024**2,expected-count+1))
                    except (TimeoutError,ConnectionError,http.client.IncompleteRead) as exc:raise RetryableError(str(exc)) from exc
                    except OSError as exc:
                        if isinstance(exc,ssl.SSLCertVerificationError):raise IntegrityError('TLS certificate failure') from exc
                        raise RetryableError(str(exc)) from exc
                    if not b:break
                    out.write(b);h.update(b);count+=len(b)
                    if count>expected:raise IntegrityError('Range body overflow')
                if count!=expected:raise RetryableError('Short range body / premature EOF')
            good=partial.with_suffix('.ok');os.replace(partial,good)
            r.update(path=str(good),sha256=h.hexdigest());budget.finish(r,'complete')
            return {'path':str(good),'start':start,'end':end,'bytes':expected,'sha256':h.hexdigest(),'etag':found}
        except BaseException as exc:
            error=exc;r['observed_prefix_sha256']=h.hexdigest();budget.finish(r,'failed',exc)
        if not isinstance(error,RetryableError) or attempt==settings['attempts']:raise error
        sleep(max(settings['backoff_seconds'][attempt-1],error.delay))
    raise IntegrityError('Range attempts exhausted')


def assemble(item,pieces,prefix,target):
    target=Path(target);partial=target.with_name(target.name+'.assembling')
    if target.exists() or partial.exists():raise IntegrityError('No assembly overwrite')
    md5=hashlib.md5();sha=hashlib.sha256();offset=0
    with partial.open('xb') as out:
        if prefix:
            if Path(prefix['path']).stat().st_size!=prefix['bytes']:raise IntegrityError('Prefix size changed')
            psha=hashlib.sha256()
            with Path(prefix['path']).open('rb') as f:
                for b in iter(lambda:f.read(1024**2),b''):out.write(b);md5.update(b);sha.update(b);psha.update(b);offset+=len(b)
            if psha.hexdigest()!=prefix['sha256']:raise IntegrityError('Prefix hash changed')
        for piece in sorted(pieces,key=lambda x:x['start']):
            path=Path(piece['path'])
            if piece['start']!=offset or path.stat().st_size!=piece['bytes'] or digest_file(path)!=piece['sha256']:
                raise IntegrityError('Gap, overlap or changed range block')
            with path.open('rb') as f:
                for b in iter(lambda:f.read(1024**2),b''):out.write(b);md5.update(b);sha.update(b);offset+=len(b)
        out.flush();os.fsync(out.fileno())
    if offset!=int(item['compressed_bytes']) or md5.hexdigest()!=item['md5']:raise IntegrityError('Complete-file length/MD5 mismatch')
    with partial.open('rb') as f:
        if f.read(2)!=b'\x1f\x8b':raise IntegrityError('Complete input is not gzip')
    os.replace(partial,target)
    return {'path':str(target),'bytes':offset,'md5':md5.hexdigest(),'sha256':sha.hexdigest(),'status':'verified_complete'}


def download(item,directory,budget,prefix=None,settings=None,opener=None,sleep=time.sleep):
    cfg=settings or SETTINGS;directory=Path(directory);target=directory/Path(item['url']).name
    parts=directory/(target.name+'.ranges');parts.mkdir()
    if target.exists():raise IntegrityError('No input overwrite')
    total=int(item['compressed_bytes']);stop=threading.Event();pieces=[];etag=None;start=0;probe=None
    if prefix:
        path=Path(prefix['path'])
        if not 0<prefix['bytes']<total or path.stat().st_size!=prefix['bytes'] or digest_file(path)!=prefix['sha256']:
            raise IntegrityError('Old prefix integrity mismatch')
        with path.open('rb') as f:
            if f.read(2)!=b'\x1f\x8b':raise IntegrityError('Old prefix is not gzip')
        start=prefix['bytes'];n=min(cfg['overlap_bytes'],start)
        probe=one_range(item,start-n,start-1,parts,budget,cfg,stop,opener=opener,sleep=sleep)
        with path.open('rb') as f:f.seek(start-n);expected=f.read(n)
        if Path(probe['path']).read_bytes()!=expected:raise IntegrityError('Remote overlap differs from old prefix')
        etag=probe['etag']
    else:
        first=one_range(item,0,min(cfg['chunk_bytes'],total)-1,parts,budget,cfg,stop,opener=opener,sleep=sleep)
        pieces.append(first);start=first['end']+1;etag=first['etag']
    todo=blocks(start,total,cfg['chunk_bytes'])
    with ThreadPoolExecutor(max_workers=cfg['workers']) as pool:
        futures=[pool.submit(one_range,item,a,b,parts,budget,cfg,stop,etag,opener,sleep) for a,b in todo]
        try:
            for f in as_completed(futures):pieces.append(f.result())
        except BaseException:
            stop.set()
            for f in futures:f.cancel()
            raise
    result=assemble(item,pieces,prefix,target)
    result.update(reused_prefix_bytes=prefix['bytes'] if prefix else 0,range_blocks=len(pieces),remote_overlap_bytes=min(cfg['overlap_bytes'],prefix['bytes']) if prefix else 0)
    save(directory/(target.name+'.verified.json'),result)
    for p in pieces+([probe] if probe else []):Path(p['path']).unlink()
    return target
