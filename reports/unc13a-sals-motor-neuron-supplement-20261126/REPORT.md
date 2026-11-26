# UNC13A in a patient-derived SALS motor-neuron cohort: supplement audit — 26 November 2026

## Question

Does the 2025 patient-derived motor-neuron cohort report the same UNC13A cryptic-splicing event studied in the canonical TDP-43-loss literature, and does its supplement place that cluster in the reported overlap with TDP-43-knockdown-responsive genes?

## Source and review method

This is a documentary review of the article and the supplied supplementary workbook, not a new RNA-seq analysis. The article studied day-49 iPSC-derived motor neurons and reports an RNA-seq comparison of 65 sporadic ALS (SALS) donors and 12 healthy controls. Its splicing analysis extracted and annotated exon junctions with RegTools 1.0.0 and tested clusters with LeafCutter 0.2.9, using a design matrix including disease type and sex and an adjusted-P threshold of 0.05.

The reviewed workbook was identified by SHA-256 `364e4368a1c560b83ebf6acc93822f4d704ba74fb0d68293ac097be1f0d7d71d`. Inspection was limited to supplementary Tables 6–8 and the article's corresponding description.

## Evidence

- Supplementary Table 7 lists the negative-strand LeafCutter cluster `chr19:clu_24564_-`, annotated to **UNC13A**, as differentially spliced between SALS and controls: log-likelihood ratio 11.59375, 4 degrees of freedom, nominal (P=0.000116159), adjusted (P=0.0156352).
- Table 6 also lists this cluster. Table 7 gives a cluster identifier and gene annotation, but not the member junction coordinates needed to map it unambiguously to a specific cryptic exon.
- Table 8 is the article's list of SALS/control splicing clusters that overlap genes responsive to TDP-43 knockdown. **UNC13A is not listed among its 18 rows.** This table-level non-listing does not establish that the reported UNC13A event is unrelated to TDP-43; it means the supplied overlap table does not document that specific cluster as part of the overlap.
- The article itself describes UNC13A mis-splicing and cryptic-exon expression in the cohort, while stating that the UNC13A and STMN2 sites differ from sites previously reported after TDP-43 depletion or in ALS cortical neurons.

## Interpretation

The supplement adds a useful distinction to the project's evidence map: this cohort has a statistically significant, patient-derived SALS-versus-control **UNC13A cluster-level association**, but the inspected tables do not resolve its exact event coordinates or establish identity with the canonical TDP-43-associated UNC13A cryptic exon. The reported site difference makes direct event-level mapping especially important.

This is literature evidence reported by the study, not a computational reproduction by this project. It is not independent functional validation of the canonical event, a demonstration of neuronal rescue, or clinical evidence.

## Limitations

- No junction-level coordinates or per-sample junction counts for this cluster are given in the inspected supplementary tables.
- Table 8's absence of UNC13A is an absence from that table's specified overlap list, not evidence of biological absence or proof against TDP-43 involvement.
- No new reads, statistical model, or sample-level unit map were analyzed here.
- The article says linked clinical, DNA-sequencing and RNA-sequencing data are intended for controlled EGA access through the ID-MND initiative; the available supplement alone does not supply the event-level mapping required for this comparison.
- These observations do not establish a causal mechanism or treatment relevance and make no claim about clinical benefit.

## Next discriminating evidence

Revisit only if an accessible, permission-compatible source provides the cluster's member junction coordinates or sample-level junction counts together with verified donor/culture identities. First map the exact event and confirm independent experimental units; only then decide whether a prospectively specified comparison with the canonical UNC13A cryptic event is warranted. No additional analysis or access request is scheduled by this report.

## References

1. Bye et al. *Large-scale drug screening in iPSC-derived motor neurons from sporadic ALS patients identifies a potential combinatorial therapy*. **Nature Neuroscience** (2025). [https://doi.org/10.1038/s41593-025-02118-7](https://doi.org/10.1038/s41593-025-02118-7).
2. Ma et al. *TDP-43 represses cryptic exon inclusion in the FTD-ALS gene UNC13A*. **Nature** (2022). [https://doi.org/10.1038/s41586-022-04424-7](https://doi.org/10.1038/s41586-022-04424-7).
