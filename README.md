# reddit_abathor
A bot for reddit (That only works on wallstreetbets, investing, and robinhood) that does on the fly statistical analysis. Use this to win internet arguments. 

It's not the kind of bot that's going to comment on your post out of the blue, it's one that you need to explicitly invoke. 

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


### Fututre commands.
Thinking of doing something that will tell you portfolio performance over time & how your portfolio would have done if you a) market hedged and b) inversed it while market hedging. 


.... More commands being added over time. 
