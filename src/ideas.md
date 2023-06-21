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

### Current status (21. 6. 202)

- Adding historical data has tanked the model's performance. It clearly overfits, as seen by the fact that the training and test accuracies are 10% apart.
- One can also obsere that the split between good and bad numbers is no longer very sharp, rather, it is quite smooth.
- It would be good to know whether this is due to poor feature selection, or whether the target variable is not well defined
- w.r.t the above point: the target variable still seems to follow a Gaussian, which is reassuring

