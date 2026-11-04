# Data-only reproduction of the public Dox block; no biological inference.
# Source: frattalab/unc13a_cryptic_splicing, e05e872, paper_figures.Rmd L3779ff.
suppressPackageStartupMessages(library(dplyr))
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
out <- args[[2]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
Protein <- read.csv(args[[1]], colClasses = c("factor", "factor", "numeric", "factor", "factor"))
Protein$Treatment <- factor(Protein$Treatment, levels=c("NT","Dox-1","Dox-2","Dox-3","Dox-4","Dox-5"))
Protein$Line_Group <- factor(Protein$Line_Group, levels=c("Protein","RNA","Correct_RNA"))
agg <- aggregate(Value~Treatment*Gene*Line_Group*Color_Group, data=Protein, FUN="mean")
std <- function(x) sd(x) / sqrt(length(x))
tmp <- Protein %>% group_by(Treatment,Gene,Line_Group,Color_Group) %>% summarise(se=std(Value))

# Original order, including dplyr's implicit common-column join.
original <- agg %>% filter(Gene != "13A-RNA") %>%
  mutate(Line_Group=gsub("Correct_RNA","RNA",Line_Group)) %>% left_join(tmp)
# Comparator: join on original keys, then change the display label.
keys <- c("Treatment","Gene","Line_Group","Color_Group")
preserved <- agg %>% filter(Gene != "13A-RNA") %>%
  left_join(tmp, by=keys) %>% mutate(Line_Group=gsub("Correct_RNA","RNA",Line_Group))
stopifnot(nrow(Protein)==138L, nrow(agg)==42L, nrow(original)==36L,
          sum(is.na(original$se))==6L, sum(is.na(preserved$se))==0L,
          identical(original$Value,preserved$Value),
          all(as.character(original$Gene[is.na(original$se)])=="13A-Correct RNA"))

# Compare the two R executions with the committed Python outputs by explicit keys.
check_python <- function(actual, filename) {
  expected <- read.csv(file.path("reports/fratta-dox-replay-20261104",filename),
                       stringsAsFactors=FALSE, na.strings="")
  actual <- as.data.frame(actual)
  for (key in keys) actual[[key]] <- as.character(actual[[key]])
  paired <- merge(actual,expected,by=keys,all=TRUE)
  stopifnot(nrow(paired)==36L, !anyNA(paired$Value), !anyNA(paired$mean),
            max(abs(paired$Value-paired$mean))<1e-12,
            identical(is.na(paired$se),is.na(paired$sem_rows)))
  keep <- !is.na(paired$se)
  stopifnot(max(abs(paired$se[keep]-paired$sem_rows[keep]))<1e-12)
}
check_python(original,"source-order-join.csv")
check_python(preserved,"key-preserving-join.csv")
write.csv(agg,file.path(out,"means-R.csv"),row.names=FALSE)
write.csv(original,file.path(out,"source-order-join-R.csv"),row.names=FALSE)
write.csv(preserved,file.path(out,"key-preserving-join-R.csv"),row.names=FALSE)
writeLines(capture.output(sessionInfo()),file.path(out,"sessionInfo.txt"))
result <- sprintf(paste0('{"R_version":"%s","dplyr_version":"%s",',
                         '"source_rows":138,"groups":42,"plot_groups":36,',
                         '"original_missing_sem":6,"preserved_missing_sem":0,',
                         '"means_unchanged":true,"Python_R_match_tolerance":1e-12,',
                         '"Python_R_match":true,"functional_inference":false}'),
                  getRversion(),packageVersion("dplyr"))
writeLines(result,file.path(out,"result.json"))
cat("FRATTA_R_RESULT_BEGIN\n",result,"\nFRATTA_R_RESULT_END\n",sep="")
