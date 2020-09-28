import matplotlib.pyplot as plt
import numpy as np
import math
from utils import split_data, get_bow, get_word_freq
from baselines import BaselineRuleBased
from ML_algorithms import train_decision_tree, train_gaussian_nb, train_multinomial_nb, train_logistic_regresor,\
    train_sktree, print_results
from dialog_system import DialogSystem
import pandas as pd

# Loading the data for the dialog acts and utterance contents
'''dialog_acts = open("dialog_acts.dat", 'r')

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

baseline_2 = BaselineRuleBased(y_train)

frequent_words = get_word_freq(X_train)

vect_X_train = get_bow(X_train, frequent_words)
vect_X_test = get_bow(X_test, frequent_words)

sktree = train_sktree(vect_X_train, y_train)
y_pred = sktree.predict(vect_X_test)
print_results(y_test, y_pred)

logistic_regressor = train_logistic_regresor(vect_X_train, y_train)
y_pred = logistic_regressor.predict(vect_X_test)
print_results(y_test, y_pred)

gaussion_nb = train_gaussian_nb(vect_X_train, y_train)
y_pred = gaussion_nb.predict(vect_X_test)
print_results(y_test, y_pred)

multinomial_nb = train_multinomial_nb(vect_X_train, y_train)
y_pred = multinomial_nb.predict(vect_X_test)
print_results(y_test, y_pred)

#decision_tree = train_decision_tree(vect_X_train, y_train)
#y_pred = decision_tree.predict(vect_X_test)
#print_results(y_test, y_pred)


model_list = [sktree, logistic_regressor, gaussion_nb, multinomial_nb]

if __name__ == '__main__':

    print('Type:\n'
          ' - 0 for SK Tree\n'
          ' - 1 for Logistic Regressor\n'
          ' - 2 for Custom decision tree\n'
          ' - 3 for Gaussian Naive Bayes\n'
          ' - 4 for Multinomial Naive Bayes\n'
          ' - 5 for Baseline\n')

    model = int(input())

    if model == 5:
        while True:
            print('type an utterance or exit to exit')
            input_text = str(input()).lower()
            if input_text == 'exit':
                break
            else:
                print(baseline_2.predict(input_text))
    else:
        while True:
            print('type an utterance or exit to exit')
            input_text = str(input()).lower()
            if input_text == 'exit':
                break
            else:
                input_text = input_text.split(' ')
                input_vector = get_bow_unpacked(input_text, frequent_words)
                print(model_list[model].predict(input_vector))'''

if __name__ == '__main__':
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


    X_train, X_test, y_train, y_test = split_data(dialog_acts)

    baseline_2 = BaselineRuleBased(y_train)

    frequent_words = get_word_freq(X_train)

    vect_X_train = get_bow(X_train, frequent_words)
    vect_X_test = get_bow(X_test, frequent_words)

    sktree = train_sktree(vect_X_train, y_train)
    y_pred = sktree.predict(vect_X_test)
    print_results(y_test, y_pred)

    ds = DialogSystem('restaurants_info.csv', sktree, frequent_words)

    while True:
        ds.get_message()
        input_text = str(input()).lower()
        if input_text == 'exit':
            break
        else:
            intent = ds.process_sentence(input_text)
            print(intent)


