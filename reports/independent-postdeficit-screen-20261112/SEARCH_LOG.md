# Finite search and access log

Date: 12 November 2026. Repository protocol commit `bac77055aa0e7eaaab9cced0513ef1cbb19819d5` preceded the first external query. Queries were documentary discovery, not effect estimation. Exact text below preserves the finite scope; returned-hit counts are not used as evidence of absence.

| Group | Search engine | Queries | Disposition |
|---|---|---|---|
| 1 | web system2 | `TDP-43 motor recovery suppression established motor deficits Walker 2015 rNLS8`; `stathmin-2 restoration treatment after motor deficit measured recovery STMN2`; `UNC13A delayed treatment functional deficit recovery baseline` | Select C1 Walker; select C2 new STMN2/Matson preprint. Keuss/Baughn/Beccari/Melamed are prior work, not new candidates. Hur 2022 belongs to the rNLS8 lead. |
| 2 | web system1, verification | `TDP-43 recovery doxycycline reintroduction motor deficits treatment baseline independent rNLS8` (3650-day filter); `STMN2 stathmin-2 delayed restoration established motor deficits treatment recovery` (730 days); `"UNC13A" "after" "deficit" "treatment"` (730 days) | Corroborates primary Walker source and prior-source exclusions. No extra candidate. Date filters constrain discovery, not the study eligibility date. |
| 3 | web system2 | `"TDP-43" "reversible" "motor deficits" doxycycline recovery rat`; `"Stathmin-2 regulates microtubule dynamics" restoration rescue methods` | Select C3 Huang/JCI59130. Alfieri and other returns not selected; no fourth dossier. |
| 4 | web system1, targeted metadata | `site:biorxiv.org/content/10.64898/2026.11.07.764673 "Stathmin" "rescue"`; `site:biorxiv.org/content/10.64898/2026.11.07.764673 "Data" "neurons"`; `site:biorxiv.org/content/10.64898/2026.11.07.764673 authors` | Indexed primary author list/abstract/posted date/licence recovered. Secondary summaries and Gomberg spillover not used to infer methods. Discovery budget exhausted. |

## Primary routes and actual artifacts

- C1: PMC5127391 article readable via web; local direct article request returned a 5,581-byte challenge response, not the article. Methods and Fig.8 legend read in web view. Supplement link: web challenge; direct bounded retrieval likewise HTML (21,574 bytes), not PDF. DOI publisher route failed. Stop; unseen supplement cannot be declared table-free. Figure-only PMC route also returned a challenge; no digitization.
- C2: direct `v1.full` inaccessible; `v1` landing HTTP403. Indexed primary record provides abstract and authors, posted 9 November, CC BY 4.0. No third direct artifact route, PDF/supplement download, detailed methods or secondary full-text substitution.
- C3: JCI article readable and locally retrieved. Supplement landing lists a 14.53MB PDF and four video links. Web PDF retrieval failed, but bounded local retrieval succeeded: PDF header verified, nine pages, no embedded files (`pdfdetach -list`). All pages extracted with `pdftotext -layout`; p.9 rendered and visually checked for the marked-rat temporal link. Supplement contains figures S1–S8 and video legends, not a verified numerical longitudinal data table. No videos downloaded. JCI Fig.4-only web route returned HTTP502; main legend remains readable. No claim that every possible supplementary route was searched.
- Family check only: Hur 2022 PMC9107273 article/author list, Fig.1 and Associated Data read; same rNLS8 investigators/model, not counted as independent. Linked supplemental-figures DOCX listed but not downloaded. No follow-up effect calculation.

`sources.json` distinguishes readable web material, successful binary retrieval, and challenge/error responses. Hashes of blocked-response bytes do not authenticate scientific article/PDF content. Primary documents stay outside git; only original review records and retrieval metadata are committed. Downloads used a 16MiB per-file read cap and 25-second request timeout; no raw sequencing, imaging collection or other mass data was acquired.

## Nondiscovery and closure

No primary-source hit was promoted merely because it said “recovery,” “rescue,” or “after.” C2 remains weak/unresolved rather than being converted into a therapeutic experiment. No sources replaced after adverse eligibility findings. Three selected families, four query groups, eleven queries: selection stops. This is not a systematic review, notice/retraction audit, exhaustive repository search, or proof against alternative explanations.

## Review correction — 12 November 2026

The eleven original discovery queries above remain historical. This review introduced no new candidate: targeted searches rechecked Walker's Results/legend/design locators, and a direct request to the public bioRxiv API retrieved Matson's complete abstract/metadata (HTTP200, hash in `matson_api_metadata.json`). The API was missing from the original method. The API-linked JATS XML returned HTTP403 here; another reviewer's reported HTTP429 is not reproduced or relabelled as this session's result. A failure in one client/route is not global source inaccessibility. Original JCI binary success/hash is retained; a different session's DNS failure does not invalidate it. C2 is now discarded at abstract triage; its full-paper contents are not declared exhaustively read. No new literature discovery cycle, SRA enumeration or count-file download was performed.
