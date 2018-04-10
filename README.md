# reddit_abathor
A bot for reddit that does on the fly statistical analysis. Use this to win internet arguments. 

## commands
### Regress command
Abathor:regress(dependant ticker, independantticker1, independantticker2..., .., .. )! 

basically you type in the command as a comment on reddit and it will spit the output of a full factormodel as a reply. 

So if some scrub says I think gold is correlated to the microsoft you can just type in: 

Abathor:regress(MSFT, GDX)! as a comment and BAM it tells you if said scrub is wrong
and then you tell the scrub that he's wrong and you have the regression results right there to really let em know he's wrong.

Nerd details:
It does an OLS regression on the day to day percent changes over the last year. It also adds a coefficient automatically. 
I only use one year of data because the coefficent isn't a constant and I figure if you're using it for talking about the market, you want an up to date estimate 
( If underlying truths change and you don't realize that, you're the scrub).

