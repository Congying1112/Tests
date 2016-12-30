#! /path/to/Rscript

stripchart(list("pass"=scan('pass.txt'), "fail"=scan('fail.txt')),
 main="Multiple stripchart for comparision",
 xlab="Degree Fahrenheit",
 ylab="Temperature",
 method="stack",
 col=c("orange","red"),
 pch=16
)
#stripchart(m, col="blue", method="stack", pch=21, cex=2,
#bg= rainbow(quantile(m, prob=c(.2, .4, .6, .8, 1), na.rm=T),alpha=0.5))
#
#boxplot(melt$value ~ melt$variable, notch=T, col=c(bpColor[1], bpColor[4]), outline=F, varwidth=T)
#stripchart(melt[melt$variable == "a", "value"] ~ melt[melt$variable == "a", "variable"], add=T, vertical=T, pch=21, bg=c(bpColor[2]), method='jitter', jitter=0.02)
#stripchart(melt[melt$variable == "b", "value"] ~ melt[melt$variable == "b", "variable"], add=T, vertical=T, pch=21, bg=c(bpColor[3]), method='jitter', jitter=0.02)
