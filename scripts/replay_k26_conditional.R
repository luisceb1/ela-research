#!/usr/bin/env Rscript
# Conditional published-source-block replay only; strict FR-K26-4d v1 remains closed.
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 2L) stop('Usage: Rscript replay_k26_conditional.R OBSERVATIONS_CSV OUTPUT_DIR')
input <- args[1]; out <- args[2]; dir.create(out, recursive=TRUE, showWarnings=FALSE)
expected_sha <- '971ab59ed7b0f021f776944d01f99b3e4eeb67465e5d43fbf939fc3dcd5e2cda'
sha_line <- system2('sha256sum', shQuote(input), stdout=TRUE)
if (!length(sha_line) || strsplit(sha_line[1], '[[:space:]]+')[[1]][1] != expected_sha) stop('Adapted CSV hash mismatch')
suppressPackageStartupMessages(library(lme4))
suppressPackageStartupMessages(library(lmerTest))
d <- read.csv(input, stringsAsFactors=FALSE, check.names=FALSE)
if (!identical(names(d), c('source_cell','source_batch','condition','value_nA','source_numeric_text'))) stop('Unexpected schema')
if (nrow(d) != 89L || anyDuplicated(d$source_cell) || any(!is.finite(d$value_nA)) || any(d$value_nA < 0)) stop('Invalid observations')
if (!identical(sort(unique(d$source_batch)), c('Batch 1','Batch 2','Batch 3'))) stop('Unexpected source blocks')
expected_counts <- c(Control=34L, KD=30L, KD_ASO=25L)
if (!identical(as.integer(table(d$condition)[names(expected_counts)]), as.integer(expected_counts))) stop('Count mismatch')
if (any(table(d$source_batch,d$condition) == 0L)) stop('Incomplete source block')
d$condition <- factor(d$condition, levels=c('KD','Control','KD_ASO'))
d$source_batch <- factor(d$source_batch, levels=c('Batch 1','Batch 2','Batch 3'))
d$log1p_value <- log1p(d$value_nA)
writeLines(c('Conditional replay; original nA values, author-labelled source blocks.',
             'Strict v1 gate NOT passed. No independent biological replication.',
             paste('Input SHA256:',expected_sha), paste('R:',R.version.string),
             paste('lme4:',packageVersion('lme4')), paste('lmerTest:',packageVersion('lmerTest'))),
           file.path(out,'execution_provenance.txt'))
writeLines(capture.output(sessionInfo()), file.path(out,'sessionInfo.txt'))

contrast_table <- function(fit, label) {
  sm <- summary(fit, ddf='Satterthwaite'); cc <- coef(sm)
  wanted <- c('conditionKD_ASO','conditionControl')
  if (!all(wanted %in% rownames(cc))) stop('Expected prespecified contrasts absent')
  ctab <- cc[wanted,,drop=FALSE]; critical <- qt(0.975, ctab[,'df'])
  data.frame(model=label, contrast=c('KD_ASO - KD','Control - KD'),
             estimate=ctab[,'Estimate'], se=ctab[,'Std. Error'], df=ctab[,'df'],
             t=ctab[,'t value'], p_nominal=ctab[,'Pr(>|t|)'],
             ci95_low=ctab[,'Estimate']-critical*ctab[,'Std. Error'],
             ci95_high=ctab[,'Estimate']+critical*ctab[,'Std. Error'],
             p_holm_two_contrasts=p.adjust(ctab[,'Pr(>|t|)'], method='holm'),
             row.names=NULL, check.names=FALSE)
}

fit_one <- function(data, scale, label) {
  warnings <- character(); messages <- character()
  formula <- if (scale=='log1p') log1p_value ~ condition + (1|source_batch) else value_nA ~ condition + (1|source_batch)
  object <- tryCatch(withCallingHandlers(lmerTest::lmer(formula, data=data, REML=TRUE),
       warning=function(w) { warnings <<- c(warnings,conditionMessage(w)); invokeRestart('muffleWarning') },
       message=function(m) { messages <<- c(messages,conditionMessage(m)); invokeRestart('muffleMessage') }),error=function(e)e)
  if (inherits(object,'error')) return(list(fit=NULL,diagnostic=data.frame(model=label,n=nrow(data),blocks=nlevels(droplevels(data$source_batch)),status='failed',error=conditionMessage(object),stringsAsFactors=FALSE)))
  vc <- as.data.frame(VarCorr(object)); res <- residuals(object); sh <- shapiro.test(res)
  convergence <- unlist(object@optinfo$conv$lme4$messages)
  diagnostic <- data.frame(model=label,n=nrow(data),blocks=nlevels(droplevels(data$source_batch)),
      status='fitted',singular=isSingular(object),batch_variance=vc$vcov[vc$grp=='source_batch'][1],
      residual_sd=sigma(object),shapiro_W=unname(sh$statistic),shapiro_p=sh$p.value,
      gaussian_assumption_flag=unname(sh$statistic)<0.90,
      optimizer=paste(object@optinfo$optimizer,collapse=';'),
      optimizer_code=paste(unlist(object@optinfo$conv$opt),collapse=';'),
      convergence_messages=paste(convergence,collapse=';'),warnings=paste(warnings,collapse=';'),
      messages=paste(messages,collapse=';'),stringsAsFactors=FALSE)
  writeLines(capture.output(summary(object,ddf='Satterthwaite')), file.path(out,paste0(label,'_summary.txt')))
  write.csv(data.frame(source_cell=data$source_cell,source_batch=data$source_batch,condition=data$condition,
                       fitted=fitted(object),residual=res),file.path(out,paste0(label,'_residuals.csv')),row.names=FALSE)
  list(fit=object,contrasts=contrast_table(object,label),diagnostic=diagnostic)
}

# Independent arithmetic check of the t-interval extraction on a known constant.
stopifnot(abs(qt(0.975,10)-2.22813885196494)<1e-10)
primary <- fit_one(d,'log1p','primary_log1p')
if (is.null(primary$fit)) stop('Primary model failed; inspect logs, no estimate substituted')
raw <- fit_one(d,'raw','raw_scale_sensitivity')
write.csv(primary$contrasts,file.path(out,'primary_contrasts.csv'),row.names=FALSE)
if (!is.null(raw$fit)) write.csv(raw$contrasts,file.path(out,'raw_scale_contrasts.csv'),row.names=FALSE)
# A nonconvergence diagnostic may not replace the retained primary fit.
if (length(primary$fit@optinfo$conv$lme4$messages) && !isSingular(primary$fit)) {
  diagnostic_refit <- try(lmerTest::lmer(log1p_value~condition+(1|source_batch),data=d,REML=TRUE,
                          control=lmerControl(optimizer='bobyqa')),silent=TRUE)
  writeLines(capture.output(diagnostic_refit), file.path(out,'bobyqa_diagnostic_only.txt'))
}

loo <- list(); diagnostics <- list(primary$diagnostic,raw$diagnostic)
for (batch in levels(d$source_batch)) {
  subset <- droplevels(d[d$source_batch!=batch,,drop=FALSE]); label <- paste0('without_',gsub(' ','_',batch))
  current <- fit_one(subset,'log1p',label); diagnostics[[length(diagnostics)+1]] <- current$diagnostic
  if (!is.null(current$fit)) {
    row <- current$contrasts[current$contrasts$contrast=='KD_ASO - KD',,drop=FALSE]
    row$omitted_batch <- batch; row$singular <- isSingular(current$fit); loo[[length(loo)+1]] <- row
  }
}
if (length(loo)) write.csv(do.call(rbind,loo),file.path(out,'leave_one_batch_out.csv'),row.names=FALSE)
# All expected fits are represented; failure rows have explicit missing fields.
columns <- unique(unlist(lapply(diagnostics,names)))
diagnostics <- lapply(diagnostics,function(x){for(n in setdiff(columns,names(x)))x[[n]]<-NA;x[,columns,drop=FALSE]})
write.csv(do.call(rbind,diagnostics),file.path(out,'model_diagnostics.csv'),row.names=FALSE)

summaries <- list()
for (batch in levels(d$source_batch)) for (cond in levels(d$condition)) {
  v <- d$value_nA[d$source_batch==batch & d$condition==cond]
  summaries[[length(summaries)+1]] <- data.frame(source_batch=batch,condition=cond,n=length(v),
                                               mean_nA=mean(v),median_nA=median(v),sd_nA=sd(v))
}
sums <- do.call(rbind,summaries); write.csv(sums,file.path(out,'batch_condition_summaries.csv'),row.names=FALSE)
differences <- do.call(rbind,lapply(levels(d$source_batch),function(batch){
  s <- sums[sums$source_batch==batch,]; v <- setNames(s$mean_nA,s$condition)
  data.frame(source_batch=batch,ASO_minus_KD_nA=unname(v['KD_ASO']-v['KD']),
             Control_minus_KD_nA=unname(v['Control']-v['KD']))
}))
write.csv(differences,file.path(out,'batch_mean_differences.csv'),row.names=FALSE)
equal_means <- sapply(levels(d$condition),function(cond)mean(sums$mean_nA[sums$condition==cond]))
numerator <- unname(equal_means['KD_ASO']-equal_means['KD']); denominator <- unname(equal_means['Control']-equal_means['KD'])
stable <- denominator>0 && all(differences$Control_minus_KD_nA>0)
write.csv(data.frame(mean_KD_nA=unname(equal_means['KD']),mean_Control_nA=unname(equal_means['Control']),
                     mean_KD_ASO_nA=unname(equal_means['KD_ASO']),equal_batch_ASO_minus_KD_nA=numerator,
                     equal_batch_Control_minus_KD_nA=denominator,
                     recovery_ratio=if(stable)numerator/denominator else NA,
                     recovery_ratio_defined=stable,interpretation='descriptive, conditional; not equivalence or clinical recovery'),
          file.path(out,'equal_batch_descriptive.csv'),row.names=FALSE)

png(file.path(out,'residual_diagnostics.png'),width=1400,height=1050,res=130)
par(mfrow=c(2,2),mar=c(4,4,3,1))
for (item in list(primary,raw)) {
  if (!is.null(item$fit)) {
    qqnorm(residuals(item$fit),main=paste(item$diagnostic$model,'Q-Q'));qqline(residuals(item$fit),col='red')
    plot(fitted(item$fit),residuals(item$fit),xlab='Fitted',ylab='Residual',main=item$diagnostic$model);abline(h=0,lty=2)
  }
}
dev.off()
writeLines(capture.output(primary$contrasts),file.path(out,'primary_contrasts.txt'))
cat('Completed conditional published-block replay. Strict v1 remains closed.\n')
print(primary$contrasts)
