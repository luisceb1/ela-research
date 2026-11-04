"""Summarize reduced administrative observations. No network, mailbox or data access."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
from zoneinfo import ZoneInfo


def summarize(path):
    raw=Path(path).read_bytes();record=json.loads(raw)
    notices=sorted(record['ad_workbench_notices'],key=lambda r:r['received_utc'])
    if len(notices)!=4 or any(r['has_attachments'] is not False for r in notices):raise ValueError('Observed notice inventory changed; inspect source again')
    by_kind={n['evidence_kind']:n for n in notices}
    if len(by_kind)!=4 or set(by_kind)!={'dataset_approval_wording','dataset_review_wording','workspace_submission_wording','workspace_review_wording'}:raise ValueError('Do not conflate notice stages')
    times={k:datetime.fromisoformat(v['received_utc'].replace('Z','+00:00')) for k,v in by_kind.items()}
    fig=record['fig4d']
    if (fig['known_thread_messages_seen'],fig['sent_messages_seen'],fig['incoming_messages_seen'],fig['scoped_incoming_search_results'],fig['source_data_files_received_in_checked_sources'])!=(1,1,0,0,0):raise ValueError('Source data status needs fresh inspection')
    if record['communication_sent_this_run'] or record['access_effectively_confirmed'] or record['manifest_received_in_checked_sources']:raise ValueError('This block summary cannot certify new access or data')
    return {'observed_on':record['observed_on'],'python':platform.python_version(),'observations_sha256':hashlib.sha256(raw).hexdigest(),
       'dataset_permission':'approval wording and review wording both observed; effective access not verified',
       'workspace':'review wording observed; provisioning not verified',
       'approval_notice_madrid':times['dataset_approval_wording'].astimezone(ZoneInfo('Europe/Madrid')).isoformat(),
       'review_notice_madrid':times['dataset_review_wording'].astimezone(ZoneInfo('Europe/Madrid')).isoformat(),
       'notice_interval_seconds':(times['dataset_review_wording']-times['dataset_approval_wording']).total_seconds(),
       'issue37_missing':'concrete technical manifest/file with access terms, junction counts or indexed alignments, biological-unit/batch map',
       'issue44_missing':'original Fig.4d eEPSC table with units, groups, exclusions and cell-to-culture/differentiation map',
       'new_scientific_input_received_in_checked_sources':False,'scientific_analysis_executed':False,
       'new_unit_tests_added':0,'biological_replicates_added':0,'communication_sent':False,
       'decision':'stop this research cycle under BACKLOG; resume only with concrete new input and decision',
       'scope_limit':'bounded connected-mail queries and repository records; not a portal inspection or global proof of absence'}


if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__);p.add_argument('observations');args=p.parse_args()
    print(json.dumps(summarize(args.observations),indent=2,ensure_ascii=False))
