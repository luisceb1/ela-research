#!/usr/bin/env Rscript
# Independent arithmetic checks on the already executed conditional replay.
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=1L) stop('Usage: Rscript check_k26_replay_outputs.R RESULT_DIR')
out <- args[1]
d <- read.csv(file.path(out,'observations.csv'),stringsAsFactors=FALSE)
d$condition <- factor(d$condition,levels=c('KD','Control','KD_ASO'))
d$source_batch <- factor(d$source_batch)
ct <- read.csv(file.path(out,'primary_contrasts.csv'),stringsAsFactors=FALSE)
diag <- read.csv(file.path(out,'model_diagnostics.csv'),stringsAsFactors=FALSE)
p <- diag[diag$model=='primary_log1p',]
# Reconstruct GLS coefficients/SE conditional on the fitted variance components,
# without calling lmer or the replay's coefficient-extraction function.
X <- model.matrix(~condition,d)
Z <- model.matrix(~source_batch-1,d)
V <- p$batch_variance * tcrossprod(Z) + diag(p$residual_sd^2,nrow(d))
ViX <- solve(V,X)
cov_beta <- solve(crossprod(X,ViX))
beta <- as.vector(cov_beta %*% crossprod(X,solve(V,log1p(d$value_nA))))
names(beta) <- colnames(X)
stopifnot(max(abs(beta[c('conditionKD_ASO','conditionControl')]-ct$estimate))<1e-8)
stopifnot(max(abs(sqrt(diag(cov_beta))[c('conditionKD_ASO','conditionControl')]-ct$se))<1e-8)
stopifnot(max(abs(2*pt(-abs(ct$estimate/ct$se),df=ct$df)-ct$p_nominal))<1e-12)
stopifnot(max(abs(ct$estimate-qt(.975,ct$df)*ct$se-ct$ci95_low))<1e-10)
stopifnot(max(abs(ct$estimate+qt(.975,ct$df)*ct$se-ct$ci95_high))<1e-10)
stopifnot(max(abs(p.adjust(ct$p_nominal,'holm')-ct$p_holm_two_contrasts))<1e-12)
# Verify equal-block weighting directly from source observations, not model means.
means <- aggregate(value_nA~source_batch+condition,d,mean)
v <- tapply(means$value_nA,means$condition,mean)
e <- read.csv(file.path(out,'equal_batch_descriptive.csv'))
stopifnot(abs(e$equal_batch_ASO_minus_KD_nA-(v['KD_ASO']-v['KD']))<1e-10)
stopifnot(abs(e$recovery_ratio-(v['KD_ASO']-v['KD'])/(v['Control']-v['KD']))<1e-10)
loo <- read.csv(file.path(out,'leave_one_batch_out.csv'))
stopifnot(nrow(loo)==3L,length(unique(loo$omitted_batch))==3L)
writeLines(c('PASS: GLS coefficients and SE from fitted V',
             'PASS: Satterthwaite t-tail/pointwise interval arithmetic and Holm family',
             'PASS: equal-batch summaries and descriptive recovery arithmetic',
             'PASS: three distinct leave-one-block-out results',
             'These checks validate computation, not biological independence.'),file.path(out,'arithmetic_validation.txt'))
cat('All independent arithmetic checks passed.\n')
