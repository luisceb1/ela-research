"""Emit a disabled human-scale planning envelope; never launch a stage."""
import json
from pilot_execution_policy import validate


def proposal():
    GiB=1024**3;MiB=1024**2
    limits={'wall_seconds':9000,'transfer_bytes':12_000_000_000,'disk_bytes':25*GiB,'reserve_bytes':8*GiB,'threads':2,
            'process_caps':{'wall_seconds':3600,'rss_bytes':6*GiB,'address_space_bytes':8*GiB}}
    phases={}
    def phase(name,kind,wall,rss,space,**extra):phases[name]={'kind':kind,'wall_seconds':wall,'rss_bytes':rss,'address_space_bytes':space,**extra}
    phase('preflight','process',120,512*MiB,GiB)
    for name in ('index_archive','CTRL_R1','CTRL_R2','TDP_R1','TDP_R2'):phase(name,'transfer',3600,512*MiB,GiB)
    phase('index_extract','archive',600,GiB,2*GiB)
    for name in ('CTRL_prefix','TDP_prefix'):phase(name,'paired_fastq',900,GiB,2*GiB)
    for name in ('CTRL_compute','TDP_compute'):phase(name,'compact',1200,6*GiB,8*GiB,producer_seconds=900,reduce_seconds=300)
    policy={'schema':'pilot-b4-local-v1','production_enabled':False,'total_seconds':9000,'transfer_seconds':3600,
            'allocations':{'artifacts':16*GiB,'prefixes':2*GiB,'temporaries':6*GiB,'dependencies':512*MiB,'receipts':256*MiB},'phases':phases}
    validate(policy,limits)
    from compact_pe_pipeline import DEFAULT_LIMITS
    compute={**DEFAULT_LIMITS,'max_input_bytes':16*GiB,'max_records':16_000_000,'max_temp_bytes':6*GiB,'chunk_bytes':16*MiB,'merge_fan_in':16,'max_runs':16384,'max_targets':3}
    return {'status':'PLAN_ONLY_NOT_LAUNCHABLE','execution_enabled':False,'raw_execution_ready':False,'limits':limits,'execution_policy':policy,'compact_limits':compute,
            'clock_envelope_seconds':3600+sum(p['wall_seconds'] for p in phases.values() if p['kind']!='transfer'),
            'disk_allocated_bytes':sum(policy['allocations'].values()),'disk_unallocated_bytes':limits['disk_bytes']-sum(policy['allocations'].values()),
            'artifacts_worst_body_cap_plus_index_extracted':12_000_000_000+4_664_043_238,
            'minimum_body_plus_full_dependency_allocation':10_705_490_230+512*MiB,
            'coverage':{'minimum_fragment_union':20,'anchor':15,'unit':'accepted RG/QNAME group with at least one target, not unique molecule','event_support_sum_reported_separately':True,'on_insufficient':'stop before any new phase; no automatic expansion'},
            'remaining_before_real_execution':['B1 fixed external producer/consumer worker and origins','B5 actual index/dialect/dependencies/host verification','explicit execution decision; this plan does not enable production'],
            'limits_are_stop_caps_not_benchmarks':True,'RSS_is_sampled_group_AS_is_per_process':True}


if __name__=='__main__':print(json.dumps(proposal(),indent=2))
