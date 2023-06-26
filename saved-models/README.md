# Saved Models

This subfolder contains models, data points and labels, saved through running `../euromillions.ipynb`.
These can be loaded in using `Python`'s `pickle` library.
They are primarily used by the `../quickstart.py` script to make predictions on user inputs.

# Files

- `soft-vote-model.sav`: The soft-voting classifier used for the final prediction
- `saved-dataset.sav`: The fully cleaned euromillions dataset
- `model-labels.sav`: The model labels which are used by the soft-voting classifier to make predictions.

# Current up-to-date model

- Soft-voting model with Random Forest, C-SVM and XGBoost (for details see `../euromillions.ipynb`)
- Dated: 26. 06. 2023
- Data points: 1233
- Accuracy on training set: 67.3%
- Accuracy on test set: 67.3%
- It's confusion matrix can be found below:


![Confusion matrix](../plots/final-model-confusion-matrix.png "Confusion matrix computed on test dataset via the final predictive model.")
