# Independent-host STMN2 technical pilot closure — 26 November 2026

**Status: completed; 7/7 fixed numerical fields agree.** Evidence level: technical reproduction on a different compute host for one previously measured control library. Not independent biological replication.

## Evidence

- Prospective scope: [one-library pilot](../../infrastructure/hetzner/STMN2-PILOT.md); no new comparison, threshold adjustment or second library.
- GitHub Actions [run 45786109911](https://github.com/luisceb1/ela-research/actions/runs/45786109911), attempt 1, execution commit `9be7390f824abc5da97d303eca87f6d9f94cc019`. Both [pilot](https://github.com/luisceb1/ela-research/actions/runs/45786109911/job/139793160539) and [verify-cleanup](https://github.com/luisceb1/ela-research/actions/runs/45786109911/job/139845694073) concluded success.
- [Artifact](https://github.com/luisceb1/ela-research/actions/runs/45786109911/artifacts/15105979984) ID 15105979984, 52,618 bytes, 10 members, expires 3 December 2026 at 10:27 UTC. A separate retained copy of the original ZIP passed ZIP integrity checks and matched GitHub's SHA-256: `2db0740d4e3af3bcfa42e3c101b4afe66e8f15fbc6d44d2000811b99f5ba1bd1`. [Evidence receipt](evidence.json) preserves the aggregate record, member digests and run facts without publishing raw logs or source reads.
- The declared fixed reference in [manifest.json](../../reproduction/stmn2-six-libraries/manifest.json) equals the expected and observed records in the archived comparison; the standalone count record agrees too.

| Field | Locked reference | Observed | Match |
|---|---:|---:|:---:|
| canonical | 1945 | 1945 | yes |
| cryptic | 3 | 3 | yes |
| sam_records | 139759296 | 139759296 | yes |
| alignment_groups | 65478552 | 65478552 | yes |
| eligible_groups | 61077456 | 61077456 | yes |
| marked_duplicate_records | 0 | 0 | yes |
| rejected_groups | 4401096 | 4401096 | yes |

## Runtime and resource closure

| Clock / measure | Recorded value |
|---|---|
| Workflow (UTC) | 08:47:12–10:27:55; 1 h 40 min 43 s |
| Internal total | 5,875.695 s (1 h 37 min 56 s) |
| Replay | 3,535.841 s (58 min 56 s) |
| Controller cleanup confirmed | 10:27:33.735 UTC |
| Independent cleanup confirmed | 10:27:52.633 UTC |
| Gross server rate (pilot log) | EUR 0.268499/hour plus IPv4 |
| Estimated server cost | EUR 0.45 prorated to workflow time, or EUR 0.54 assuming two billable hours, plus IPv4; not an invoice |

Both cleanup logs explicitly report no matching pilot resources remain. This is scoped to the run's resources, not an independent census of the entire Hetzner project. The three-hour limit was not exceeded. GitHub reports nonfatal Node.js deprecation warnings. No retry, new VM, or additional library launched during closure.

## Interpretation and limitations

- The existing local six-library replay remains a same-PC result (12 event counts and 30 QC fields). The cloud result extends technical portability only for GSM8009878, not all six libraries.
- Recorded software: fastp 0.23.4 historical binary hash match; HISAT2 2.2.3 rebuilt, with a different binary digest; PySAM 0.23.3 and Python 3.12.3. Recorded input identities match the locked manifest. The closure audit verifies the archived evidence, not the original large input/index bytes on a live cloud host.
- The same biological input was reused. The 3 cryptic groups remain below the fixed descriptive diagnostic; insufficient support is not a biological zero. No new effect, ratio, functional recovery, therapeutic target, or clinical evidence.
- No change to prior UNC13A or GSE304550/PFKP results, their provenance limitations, or independent-data gates. Existing open questions are not resolved by this infrastructure success.

## Decision

Close this fixed pilot and retain the evidence. A separate decision is required before any additional paid/cloud execution, scientific analysis or publication of new results. Keep the best-effort expiry safeguard available while the disposable infrastructure is retained; no workflow or credential change is part of this documentation closure.
