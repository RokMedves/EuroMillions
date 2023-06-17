# Some ideas for the code

## New features

- See how the numbers are distributed on a Euromillions ticket. See if rows/columns/diagonals can be good features for regular numbers and whether the lucky numbers are in the same or in different rows of the ticket

## Thoughts on including older data
A long term goal is to make it possible to include old data from before Sep. 2016. A first step in this could be to change the target variable to winners/sales. In principle, this ratio should be 1/13 in today's setup (which needs to be checked!), however, it is very easy to predict in the old format. Likewise for data before May 2011, where the 2+0 group was abscent, this simplified target variable could offer valuable insight. 

Action plan:
1. Simplify the target variable to winners/sales
2. See whether the data follows the expected distributions
3. See whether the model's predictive power drops for the new variable
4. Introduce changes that would make it possible to include older data and repeat from step 2
