from sklearn import model_selection
import numpy as np


def split_data(data):
    # Function for splitting arrays in X and r
    contents = data[:, 0, None]
    acts = data[:, 1, None]

    # Split data in training and test set (85%, 15%)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(acts, contents, test_size=0.15, train_size=0.85, random_state=0)

    # Check
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    return X_train, X_test, y_train, y_test
