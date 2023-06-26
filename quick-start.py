#!/bin/python3
######################################
#
#     Euromillions Quickstart
#          by Rok Medves
#
#  This code evaluates the trained model
#  originating from euromillions.ipynb
#  on a set of user-specified numbers
#
######################################

import pickle
import numpy as np
from sklearn import ensemble
import pandas as pd
from datetime import datetime
from src.dataEng import FeatureEngineering

# For ease of use, write the model  
# date as a global variable
model_date = "26.06.2023"

class InputHelper:
    """
    Helper class that gets user input
    
    Attributes
    ----------
    year : int
        The current year

    Methods
    -------     
    print_hello()
        Prints the hello message for the start of the program

    get_user_input() -> pd.DataFrame
        Gets the user input and validates it. Returns dataframe of inputs
    
    validate_nums(self, nums, nnums = 5, nmin=1, nmax=50) -> bool
        Validates whether the user's unput was a valid EuroMillions number
    """

    def __init__(self) -> None:
        self.year = int(datetime.today().year)
        self.print_hello()

    def print_hello(self):
        """
        Prints the hello message
        """
        # ------------------------------ Some intro stuff ------------------------------ 
        print("##############################################################")
        print("#                        You are using                       #")
        print("#                   EuroMillions Quickstart                  #")
        print("#                        by Rok Medves                       #")
        print("#          https://github.com/RokMedves/EuroMillions         #")
        print(f"#                 ML model date: {model_date}                  #")
        print("#                                                            #")
        print("#        This script evaluates YOUR EuroMillions number.     #")
        print("#                                                            #")
        print("#        Lottery rules:                                      #")
        print("#        On the EuroMillions lottery you                     #")
        print("#        bet on a 7 numbers consisting of:                   #")
        print("#        -> 5 unique numbers between 1 and 50 and            #")
        print("#        -> 2 unique lucky numbers between 1 and 12          #")
        print("#        Enter these below and see how well you'd do!        #")
        print("#                                                            #")
        print("##############################################################")

    def get_user_input(self) -> pd.DataFrame:
        """
        Prompts the user to input 5 number N,
        and 2 lucky number L. 

        Returns
        -------
        pd.Dataframe
            A dataframe which can be used for feature 
            engineering and machine learning
        """

        # get 5 unique number N from user between 1 and 50
        Ns = sorted(list(map(int, input("Enter 5 unique numbers between 1 and 50 (for example 45 30 12 1 7): ").split())))
        # validate the user input
        self.validate_nums(nums = Ns, nnums = 5, nmin = 1, nmax = 50)
        Ls = sorted(list(map(int, input("Enter 2 unique lucky numbers between 1 and 12 (for example 7 12): ").split())))
        # validate the user input
        self.validate_nums(nums = Ls, nnums = 2, nmin = 1, nmax = 12)

        # create a dataframe with all the information

        tags = ['N'+str(i) for i in range(1,6,1)] + ['L1', 'L2']
        df = pd.DataFrame()
        df['YYYY'] = [self.year]
        for tag, val in zip(tags, Ns + Ls):
            df[tag] = [val]

        return df
        

    def validate_nums(self, nums, nnums = 5, nmin=1, nmax=50) -> bool:
        """
        Validates whether the user's input, nums, was
        a valid set of nnums unique Euromillions numbers
        between nmin and nmax

        Parameters
        ----------
        nums : list
            List of integers as entered by the user
        nnums: 
            The expected number of unique numbers inputed by the user
        nmin : int
            The smallest the drawn numbers are allowed to be
        nmax : int
            The largerst the drawn numbers are allowed to be
            
        Returns
        -------
        bool
            True if the input is a valid EuroMillions number
        """

        # test whether exactly nnums were entered
        #assert(len(nums)==nnums and f"Expected input to be set of {nnums} numbers; {len(nums)} were received")
        if len(nums) != nnums:
            print(f"Error: Expected to receive {nnums} numbers; {len(nums)} were received")
            exit(1)
        # test number uniqueness
        # assert(len(list(set(nums))) == nnums and "Inputs must be unique")
        if len(list(set(nums))) != nnums:
            print("Error: Inputs must be unique")
            exit(1)
        # test whether numbers are in the correct range
        # assert(all(map(lambda i: (i>=nmin) and (i<=nmax), nums)) and f"Inputs must be between {nmin} and {nmax}")
        if any(map(lambda i: (i<nmin) or (i>nmax), nums)):
            print(f"Error: Inputs must be between {nmin} and {nmax}")
            exit(1)
        

        return True

if __name__ == "__main__":

    # ------------------------------ get the user input ------------------------------ 
    # Input is handled through the InputHelper class
    
    helper = InputHelper()
    user_input = helper.get_user_input()
    user_cols = user_input.columns

    # ------------------------------ get the original dataset ------------------------------ 
    # In order to get realistically engineered features, 
    # we need to import the whole dataset.
    # 
    # Note: This is a bit of a hack. The engineered features,
    # especially the binned ones, are defined w.r.t the whole dataset
    # (for example via "pd.cut(self.data['N sum'], 6)" in sec/dataEng.py).
    # The hack here is to just append the user's data to the whole dataset
    # and reengineer all the features. While this isn't perfect, the assumption
    # is that the dataset is sufficiently large that this gives an equivalent
    # set of engineered features as in the original analysis.
    
    dataset_filename = 'saved-models/saved-dataset.sav'
    dataset = pickle.load(open(dataset_filename, 'rb'))
    user_plus_dataset = pd.concat([dataset.loc[:, user_cols], user_input])

    # ------------------------------ engineer the necessary features ------------------------------ 
    # For this we use the FeatureEngineering class located in src/dataEng.py
    eng = FeatureEngineering(user_plus_dataset)
    eng.engineer_features()
    eng.drop_unwanted_values()

        
    # ------------------------------ load the model from disk ------------------------------ 
    # This model is generated through euromillions.ipynb
    model_filename  = 'saved-models/soft-vote-model.sav'
    loaded_model  = pickle.load(open(model_filename, 'rb'))

    # ------------------------------ Load the model's used features ------------------------------ 
    # The model features are generated through euromillions.ipynb and saved on the disk
    features_filename = 'saved-models/model-lables.sav'
    model_features  = pickle.load(open(features_filename, 'rb'))
    
    # ------------------------------ Make a prediction ------------------------------ 
    
    # To evaluate the prediction, re-select the user's entry 
    # (index -1 in the user_plus_dataset DataFrame), and select only the model-relevant
    # featrues. Then, evaluate the prediction and format it nicely

    formated_input = user_plus_dataset.iloc[[-1]][model_features]

    result = loaded_model.predict_proba(formated_input)
    best_label = np.argmax(result[0])

    # a helper function
    def num_to_words(index: int) -> str:
        """
        Retruns whether 'best_label' points to 
        a good or bad betting number.
        """
        return "BAD" if not index else "GOOD"  

    # format the output and give it to the user
    print("\n--------------------------------------------------------------")
    print("The model predicts your number:\n{0}\nis a {1} number to bet on with {2:.1f}% confidence"
          .format(user_input.drop('YYYY', axis=1), num_to_words(best_label),result[0][best_label]*100))