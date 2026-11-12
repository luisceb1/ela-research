#!/usr/bin/env Rscript
# Post-hoc review clarification only; does not change the original contrast family.
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=1L) stop('Usage: Rscript review_k26_outputs.R RESULT_DIR')
out <- args[1]
suppressPackageStartupMessages(library(lmerTest))
if(as.character(getRversion())!='4.5.0' || as.character(packageVersion('lme4'))!='1.1.37' ||
   as.character(packageVersion('lmerTest'))!='3.1.3') stop('Review environment differs from original replay')
input <- file.path(out,'observations.csv')
sha <- strsplit(system2('sha256sum',shQuote(input),stdout=TRUE)[1],'[[:space:]]+')[[1]][1]
if(sha!='971ab59ed7b0f021f776944d01f99b3e4eeb67465e5d43fbf939fc3dcd5e2cda') stop('Input drift')
d <- read.csv(input,stringsAsFactors=FALSE)
d$condition <- factor(d$condition,levels=c('KD','Control','KD_ASO'))
d$source_batch <- factor(d$source_batch,levels=c('Batch 1','Batch 2','Batch 3'))
d$log1p_value <- log1p(d$value_nA)
original_diag <- read.csv(file.path(out,'model_diagnostics.csv'))
output <- list()
for(scale in c('log1p','raw')) {
  formula <- if(scale=='log1p') log1p_value~condition+(1|source_batch) else value_nA~condition+(1|source_batch)
  label <- if(scale=='log1p') 'primary_log1p' else 'raw_scale_sensitivity'
  fit <- lmerTest::lmer(formula,data=d,REML=TRUE)
  prior <- read.csv(file.path(out,if(scale=='log1p') 'primary_contrasts.csv' else 'raw_scale_contrasts.csv'))
  beta <- lme4::fixef(fit)
  stopifnot(max(abs(beta[c('conditionKD_ASO','conditionControl')]-prior$estimate))<1e-6)
  diag <- original_diag[original_diag$model==label,]
  stopifnot(abs(as.data.frame(lme4::VarCorr(fit))$vcov[1]-diag$batch_variance)<1e-6)
  L <- c(0,-1,1)
  tested <- lmerTest::contest1D(fit,L=L,ddf='Satterthwaite',confint=TRUE,level=.95)
  # Independently check the linear contrast against the fixed-effect covariance.
  est <- sum(L*beta);se <- sqrt(as.numeric(t(L)%*%as.matrix(vcov(fit))%*%L))
  stopifnot(abs(tested$Estimate-est)<1e-10,abs(tested$`Std. Error`-se)<1e-10)
  df <- tested$df;p <- 2*pt(-abs(est/se),df=df);lo <- est-qt(.975,df)*se;hi <- est+qt(.975,df)*se
  stopifnot(abs(tested$`Pr(>|t|)`-p)<1e-12)
  output[[length(output)+1]] <- data.frame(model=label,contrast='KD_ASO - Control',
      selection='post-hoc external-review clarification',estimate=est,se=se,df=df,t=est/se,
      p_nominal_exploratory=p,ci95_low_pointwise=lo,ci95_high_pointwise=hi,
      original_primary_family_unchanged=TRUE,equivalence_test_performed=FALSE,
      singular=lme4::isSingular(fit),stringsAsFactors=FALSE)
}
write.csv(do.call(rbind,output),file.path(out,'review_posthoc_ASO_Control.csv'),row.names=FALSE)
b <- read.csv(file.path(out,'batch_mean_differences.csv'))
b$block_recovery_ratio <- b$ASO_minus_KD_nA/b$Control_minus_KD_nA
b$weight_in_prespecified_aggregate <- b$Control_minus_KD_nA/sum(b$Control_minus_KD_nA)
aggregate_ratio <- sum(b$ASO_minus_KD_nA)/sum(b$Control_minus_KD_nA)
stopifnot(abs(sum(b$weight_in_prespecified_aggregate*b$block_recovery_ratio)-aggregate_ratio)<1e-12)
original <- read.csv(file.path(out,'equal_batch_descriptive.csv'))
stopifnot(abs(original$recovery_ratio-aggregate_ratio)<1e-12)
write.csv(b,file.path(out,'review_block_recovery.csv'),row.names=FALSE)
write.csv(data.frame(prespecified_ratio_of_equal_block_aggregates=aggregate_ratio,
  posthoc_unweighted_mean_of_block_ratios=mean(b$block_recovery_ratio),
  posthoc_unweighted_median_of_block_ratios=median(b$block_recovery_ratio),
  min_block_ratio=min(b$block_recovery_ratio),max_block_ratio=max(b$block_recovery_ratio),
  blocks_with_point_ratio_above_one=sum(b$block_recovery_ratio>1),
  recovery_ratio_CI_calculated=FALSE,equivalence_claim=FALSE),file.path(out,'review_ratio_summary.csv'),row.names=FALSE)
writeLines(c('PASS: same-source SHA256 and original environment',
 'PASS: unchanged full-model coefficients and batch variance reproduce before added contrast',
 'PASS: contest1D linear estimate/SE match fixed-effect covariance arithmetic',
 'PASS: contrast t-tail/pointwise interval arithmetic',
 'PASS: aggregate ratio equals deficit-weighted mean of block ratios',
 'Post-hoc contrasts and descriptive summaries do not establish equivalence.'),file.path(out,'review_arithmetic_validation.txt'))
cat('Review completed; original primary contrasts/family and strict gate unchanged.\n')
print(do.call(rbind,output));print(b)
