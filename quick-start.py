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

class InputHelper:
    """
    Helper class that gets user input
    
    Attributes
    ----------
    year : int
        The current year

    Methods
    -------
    validate_N(Ns : list) -> bool
        Validates whether the user's unput was a valid EuroMillions number
    """

    def __init__(self) -> None:
        self.year = int(datetime.today().year)

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
        Ns = sorted(list(map(int, input("Enter 5 different numbers between 1 and 50: ").split())))
        # validate the user input
        self.validate_nums(nums = Ns, nnums = 5, nmin = 1, nmax = 50)
        Ls = sorted(list(map(int, input("Enter 2 different lucky numbers between 1 and 12: ").split())))
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
        assert(len(nums)==nnums and f"Expected input to be set of {nnums} numbers; {len(nums)} were received")
        # test number uniqueness
        assert(len(list(set(nums))) == nnums and "Inputs must be unique")
        # test whether numbers are in the correct range
        assert(all(map(lambda i: (i>=nmin) and (i<=nmax), nums)) and f"Inputs must be between {nmin} and {nmax}")
        

        return True

if __name__ == "__main__":

    # ------------------------------ load the model from disk ------------------------------ 
    # This model is generated through euromillions.ipynb
    model_filename  = 'saved-models/soft-vote-model.sav'
    loaded_model  = pickle.load(open(model_filename, 'rb'))

    # ------------------------------ get the user input ------------------------------ 
    # Input in handled through the InputHelper class
    
    helper = InputHelper()
    user_input = helper.get_user_input()
    
    print(user_input)
    
    # ------------------------------ engineer the necessary features ------------------------------ 
    # For this we use the FeatureEngineering class located in src/dataEng.py
    eng = FeatureEngineering(user_input)
    eng.engineer_features()

    # ------------------------------ Load the model's used features ------------------------------ 
    # The model features are generated through euromillions.ipynb and saved on the disk
    features_filename = 'saved-models/model-lables.sav'
    model_features  = pickle.load(open(features_filename, 'rb'))
    
    # ------------------------------ Make a prediction ------------------------------ 
    result = loaded_model.predict_proba(user_input[model_features])
    print(result)