# EuroMillions
Finding good betting numbers on EuroMillions lottery.

## Introduction

I know what you are going to say: "Aren't all numbers on a lottery
equally likely?"

Yes, they are! However, the more people bet on the same numbers, the
more they have to share their winnings. An ideal number to bet on
would be one which no other person bets on, such that you get one the
winnings.

In this project a machine learning model in trained on past Euromillions
lottery winning number to infer people's betting behaviour



## Usage

1. Clone the git repo
2. Open `euromillions.ipynb` in your favourite editor
3. Run the code



## Technical details

1. The dataset information can be found in
[here](./datasets/README.md)
2. Numbers are split into "good" and "bad" numbers based on whether
the average winnings were above average or not:
3. Newly engineered features test whether the drawn numbers are
   - small
   - form a valid date
   - are "lucky" (in terms of cultural belief)
4. The final model -- a soft-voting classifier using
XGBoost, RandomForest and a C-SVM -- discerns good from bad numbers
with a 67% accuracy, indicating that there is some pattern to people's
bets

![Good and bad numbers](avg-winnings-class.pdf "Distribution of
 winnings at the lottery")

