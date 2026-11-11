# Keuss/Fratta publication and Fig.4d source-data check — 11/11/2026

## Decision

At this check, **final editorial publication is not confirmed, and no new original Fig.4d eEPSC table has been recovered**. KCL still labels the work Accepted/In press (6 October 2026). The original functional-reproduction input gate stays disabled; no effect is estimated. This is the one-time check explicitly requested by Luis on 11 November, not a new recurring search or authorization to contact Fratta again.

## Evidence

| Route inspected | Current observation | Limit |
|---|---|---|
| [KCL primary record](https://kclpure.kcl.ac.uk/portal/en/publications/unc13a-splice-correction-rescues-synaptic-dysfunction-induced-by-/) | Title UNC13A splice correction rescues synaptic dysfunction induced by TDP-43 loss; journal Nature; Accepted/In press — 6 Oct 2026. The only document link shown is an accepted author manuscript, 6.13 MB | Institutional metadata can lag editorial publication. Not proof of no final article elsewhere |
| KCL document link | The label is now UNC13A splice correction_AAM, but the underlying URL is `https://kclpure.kcl.ac.uk/portal/files/391373721/LossOfTDP_Keuss_GreenAAM.pdf`, already the historical route. Web fetch returns 403; direct metadata Python fetch also 403 | No new PDF bytes read or hashed. A renamed link is not a new source-data table |
| Crossref title query | 8 returned items; includes the 2024 preprint, 2022 Brown Nature paper/correction and other studies; none identifies the final K26 article | One ranked title query, not an exhaustive DOI-registration audit |
| Europe PMC `Keuss AND UNC13A` | 16 records returned; relevant preprint PPR871740 retains DOI 10.1101/2024.06.20.599684 | Index coverage/delay and query matching are imperfect |
| bioRxiv details API | Original DOI returns v1, 24 June 2024, `published=NA` | NA is not proof that no final publication exists |
| Directed web search, two engines | Current title, Keuss/Harley/UNC13A, Nature DOI and source-data/Zenodo/Figshare terms did not reveal a final article or attributable original Fig.4d table | Search indices can lag; no claim to have enumerated every repository |
| Gmail query `(Fratta OR Keuss) after:2026/11/02` | Two messages returned: original 3 November request and Fratta's 4 November reply. Reply anticipates the following week, no attachment. The reply was read, not inferred from memory | No new reply/file in this exact inspected query; not a complete mailbox audit |

Hashes, byte counts, query/result identities and explicit failures are in [retrieval-summary.json](retrieval-summary.json). These hashes describe public metadata responses, **not functional measurements**. The source searches use primary metadata and authoritative institutional records; unrelated review/explainer pages were not used to establish publication status.

## Version and input identity

The target is K26 accepted-manuscript Fig.4d, evoked EPSC in spinal motor neurons (declared 34 control / 30 KD / 25 KD+M21-6 cells over three experiments/differentiations). The 2024 preprint's Fig.4d is a different endpoint; its available XML is not a substitute. The [prespecified plan](../functional-rescue-20261103/REPRODUCTION_PLAN.md) requires original amplitudes/units, group and cell→culture/differentiation keys, with provenance/exclusions and independence reviewed. Neither a manuscript nor pooled sample counts opens the gate.

## Interpretation and next trigger

The defensible statement is: **no newly accessible source data was verified in the routes inspected today**. Do not turn that into a universal claim that Nature has not published it. Fratta's expected timing remains a forecast, not data delivery; the week he referred to is still in progress at this check.

Reopen #44 only on an attributable final-article/source-data URL or an original source file delivered by the authors. Inspect schema, units and biological hierarchy before fitting the prespecified model. If amplitudes arrive without the map, retain a partial-availability block; do not infer independence from cell counts or fabricate differentiation identifiers.

## Separate authorized communication

The prepared Quadros request was sent to Clotilde Lagier-Tourenne as separately authorized in the same user instruction; [log](COMMUNICATION_LOG.md). No follow-up was sent to Fratta. Source search does not authorize additional contacts or recurring checks.

Documentation/metadata-only update, no analysis or code change and no new tests required. No raw sequencing, patient records, new experiment, spending, source measurements, or treatment advice.
