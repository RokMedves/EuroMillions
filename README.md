# EuroMillions
Finding good betting numbers on EuroMillions lottery.

## Introduction

I know what you are going to say: "Aren't all numbers on the lottery
equally likely?"

Yes, they are! However, the more people bet on the same numbers, the
more they have to share their winnings. An ideal number would be one
that no other person bets on, such that you get one the winnings.

In this project a machine learning model in trained on past Euromillions
lottery winning numbers to infer people's betting behaviour.



## Usage

1. Clone the git repo
2. Open `euromillions.ipynb` in your favourite editor
3. Run the code



## Technical details

1. The dataset information can be found in
[here](./datasets).
2. Numbers are split into "good" and "bad" numbers based on whether
the average winnings were above average or not (see figure below).
3. Newly engineered features test whether the drawn numbers are
   - small;
   - form a valid date;
   - are "lucky" (in terms of cultural belief).
4. The final model -- a soft-voting classifier using
XGBoost, Random Forest and a C-SVM -- discerns good from bad numbers
with a 67% accuracy, indicating that it has learnt people's betting behaviour.

![Good and bad numbers](./plots/avg-winnings-class.pdf "Distribution of
 winnings at the lottery")

