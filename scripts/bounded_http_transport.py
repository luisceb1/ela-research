"""Bounded HTTP entity-body reader. Tests use loopback only; no execution CLI.

Budget covers bytes delivered by HTTPResponse.read1, not TCP/TLS/header traffic.
Retries are explicit full restarts, not range repair or automatic phase resume.
"""
import hashlib
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
from pilot_dry_runner import digest
from process_supervisor_v2 import atomic_json

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Redirect refused')

def transfer_http(runner,name,url,expected,allowed_origins,attempts=1,chunk_size=65536):
    parsed=urllib.parse.urlsplit(url);origin=f'{parsed.scheme}://{parsed.netloc}'
    if origin not in allowed_origins or parsed.username or parsed.password or parsed.fragment or parsed.scheme not in ('http','https'):raise ValueError('Origin or URL rejected')
    if attempts not in (1,2) or not 1<=chunk_size<=65536:raise ValueError('Unbounded retry/chunk policy')
    if expected['bytes']<0:raise ValueError('Negative expected size')
    signature=digest({'url':url,'expected':expected,'attempts':attempts,'chunk_size':chunk_size})
    if not runner.begin(name,'transfer',signature):return runner.state['phases'][name]
    phase=runner.state['phases'][name]
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    try:
        for attempt in range(attempts):
            runner.guard()
            balance=runner.state['limits']['transfer_bytes']-runner.state['transfer_bytes_consumed']
            if expected['bytes']>balance:raise RuntimeError('Insufficient body budget for full attempt')
            if expected['bytes']>runner.state['limits']['disk_bytes']:raise RuntimeError('Artifact exceeds disk cap')
            path=runner.root/f'{name}.attempt-{attempt}.partial'
            receipt=runner.root/f'{name}.attempt-{attempt}.json'
            rec={'status':'started','attempt':attempt,'body_bytes':0,'budget_scope':'HTTP entity-body read, not wire bytes'}
            atomic_json(receipt,rec)
            try:
                timeout=min(5,runner.state['deadline_epoch']-runner.clock())
                req=urllib.request.Request(url,headers={'Accept-Encoding':'identity'})
                with opener.open(req,timeout=timeout) as response,path.open('xb') as out:
                    if response.status!=200:raise ValueError('Expected full HTTP200 response')
                    if response.headers.get('Content-Encoding','identity')!='identity':raise ValueError('Encoded response refused')
                    if response.headers.get('Transfer-Encoding'):raise ValueError('Transfer-Encoding refused')
                    lengths=response.headers.get_all('Content-Length') if hasattr(response.headers,'get_all') else [response.headers.get('Content-Length')]
                    if len(lengths or [])!=1:raise ValueError('Ambiguous Content-Length')
                    if response.headers.get('Content-Length')!=str(expected['bytes']):raise ValueError('Content-Length mismatch')
                    md5=hashlib.md5();sha=hashlib.sha256()
                    while rec['body_bytes']<expected['bytes']:
                        runner.guard()
                        balance=runner.state['limits']['transfer_bytes']-runner.state['transfer_bytes_consumed']
                        amount=min(chunk_size,balance,expected['bytes']-rec['body_bytes'])
                        if amount<=0:raise RuntimeError('Body budget exhausted')
                        data=response.read1(amount)
                        if not data:raise ValueError('Truncated HTTP body')
                        runner.state['transfer_bytes_consumed']+=len(data);runner.save()
                        rec['body_bytes']+=len(data);atomic_json(receipt,rec)
                        out.write(data);out.flush();md5.update(data);sha.update(data);runner.guard()
                    os.fsync(out.fileno())
                actual_sha=sha.hexdigest()
                if md5.hexdigest()!=expected['md5'] or (expected.get('sha256') is not None and actual_sha!=expected['sha256']):raise ValueError('Hash mismatch')
                rec.update(status='verified',md5=md5.hexdigest(),sha256=actual_sha);atomic_json(receipt,rec)
                os.replace(path,runner.root/name)
                fd=os.open(runner.root,os.O_DIRECTORY)
                try:os.fsync(fd)
                finally:os.close(fd)
                phase.update(status='verified',bytes=rec['body_bytes'],md5=rec['md5'],sha256=actual_sha,attempts_used=attempt+1)
                runner.guard();runner.save();return phase
            except Exception as exc:
                rec.update(status='failed',error=f'{type(exc).__name__}: {exc}');atomic_json(receipt,rec)
                if attempt+1==attempts:raise
        raise RuntimeError('No verified attempt')
    except BaseException as exc:
        phase.update(status='failed',error=f'{type(exc).__name__}: {exc}');runner.save();raise
