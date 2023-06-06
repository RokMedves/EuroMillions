#!/bin/python3
import pickle
import numpy as np
from sklearn import ensemble
import pandas as pd

model_filename  = 'saved-models/soft-vote-model.sav'
sample_filename = 'saved-models/sample-input.sav'

# load the model from disk
loaded_model  = pickle.load(open(model_filename, 'rb'))
loaded_sample = pickle.load(open(sample_filename, 'rb'))
result = loaded_model.predict_proba(loaded_sample)
print(result)