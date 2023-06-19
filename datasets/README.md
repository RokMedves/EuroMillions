# Euro Millions dataset

By ***Rok Medves***



## Useful links

[Winning number dataset](http://lottery.merseyworld.com/cgi-bin/lottery?days=20&Machine=Z&Ballset=0&order=1&show=1&year=0&display=CSV)

[Winnings dataset](http://lottery.merseyworld.com/cgi-bin/lottery?days=20&Prizes=1&Sort=0&year=0&display=CSV)

[Sales dataset](http://lottery.merseyworld.com/Euro/Sales_index.html)

[Euromillions wiki](https://en.wikipedia.org/wiki/EuroMillions)

[Winning proportions](https://www.national-lottery.com/euromillions/odds-and-prizes)

## Remarks on dataset

1. The prize for matching any 2 numbers initially did not yield a prize.
2. The range of drawn numbers N1 -> N5 has always been between 1 and 50
3. The range of lucky numbers has changed through time: From wiki
 > The game play changed on Tuesday, 10 May 2011 with a second weekly draw and the number of "lucky stars" in the Paquerette machine increasing from 9 to 11.
 > A prize for matching two main numbers and no lucky stars was also introduced on the same date.
 > 
 > On Saturday, 24 September 2016, the number of "lucky stars" increased again, from 11 to 12. 

4. Computing the winning chance of getting n out of 5 right and l out of 2 right it's, it is (using aCb notation for *a choose b*)
  *Pr[n, l] = [5Cn * 45C(5-n)] x [2Cl * 10C(2-l)] / [50C5 x 12C2]*
 
5. The chance of winning anything given today's rules (post September 24th 2016) is 1/13

6. The lottery prizes work as follows (extracted from [this site](https://www.national-lottery.com/euromillions/odds-and-prizes))
  > There are 13 different EuroMillions prizes on offer in every draw. However, the amount you win in each tier is not a fixed amount. Instead, a percentage of the total prize fund is allocated to each category and that is split between winners. This is known as a pari-mutuel method and leads to variation in the prize amounts, because the number of tickets sold and the number of winners is always different.

  The below table describes the proportions of the prize fund allocated to the particular winning group *(N, L)*
  | Winning group (N, L) | 5+2 | 5+1 | 5+0 | 4+2 | 4+1 | 3+2 | 4+0 | 2+2 | 3+1 | 3+0 | 1+2 | 2+1 | 2+0 |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | % of prize fund | 50 | 2.61 | 0.61 | 0.19 | 0.35 | 0.37 | 0.26 | 1.30 | 1.45 | 2.70 | 3.27 | 10.30 | 16.59 |

  I have checked that the winnings do indeed follow this distribution, however, the jackpot does not due to the fact that it rolls over if nobody wins it

## Things that were wrong with the dataset

The raw downloaded dataset is not perfect and has the following quirks:

- The dataset loses a column at some point, due to a new prize category being added later (see `Remarks on dataset', point 1)
- The dataset had two swapped columns -- this became clear after analysing winning probabilities. Sadly, this makes it annoying to source the dataset from the web on every run
- The sales dataset had missing values
