import matplotlib.pyplot as plt
import numpy as np
import math
from utils import split_data
from baselines import  BaselineRuleBased

# Loading the data for the dialog acts and utterance contents
dialog_acts = open("dialog_acts.dat", 'r')

# Read in data, convert to lowercase strings
dialog_list = []
for line in dialog_acts:
    line = line.strip()
    line = line.lower()
    act = line.split(' ')[0]
    cont = line[(len(act) + 1):]
    dialog_list.append([act, cont])

dialog_acts = np.array(dialog_list)

print(dialog_acts)

X_train, X_test, y_train, y_test = split_data(dialog_acts)

baseline_2 = BaselineRuleBased()

print(baseline_2.get_classification(y_train[6]))