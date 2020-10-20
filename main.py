import numpy as np
from utils import split_data, get_bow, get_word_freq, lev_sentence
from baselines import BaselineRuleBased
from ML_algorithms import train_decision_tree, train_gaussian_nb, train_multinomial_nb, train_logistic_regressor,\
    train_sktree, print_results
from dialog_system import DialogSystem


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

    """logistic_regressor = train_logistic_regressor(vect_X_train, y_train)
    y_pred = logistic_regressor.predict(vect_X_test)
    print_results(y_test, y_pred)

    gaussion_nb = train_gaussian_nb(vect_X_train, y_train)
    y_pred = gaussion_nb.predict(vect_X_test)
    print_results(y_test, y_pred)

    multinomial_nb = train_multinomial_nb(vect_X_train, y_train)
    y_pred = multinomial_nb.predict(vect_X_test)
    print_results(y_test, y_pred)

    decision_tree = train_decision_tree(vect_X_train, y_train)
    y_pred = decision_tree.predict(vect_X_test)
    print_results(y_test, y_pred)"""

    """model_list = [sktree]


    print('Type:\n'
          ' - 0 for SK Tree\n'
          ' - 1 for Logistic Regressor\n'
          ' - 2 for Multinomial Naive Bayes\n'
          ' - 3 for Gaussian Naive Bayes\n'
          ' - 4 for Custom decision tree\n'
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
        ds = DialogSystem('restaurants_info.csv', model_list[model], frequent_words, 'similarities.json')
        while True:
            ds.get_message()
            input_text = str(input()).lower()
            lev_sentence(input_text)
            if input_text == 'exit':
                break
            else:
                intent = ds.process_sentence(input_text)
                # print(intent)"""

    ds = DialogSystem('restaurants_info.csv', sktree, frequent_words, 'similarities.json')

    print("On/Off")
    input_auto = str(input()).lower()

    rounds = 0
    mistakes = 0

    if input_auto == 'on':
        while True:
            ds.get_message()
            input_text = str(input()).lower()
            input_text, flag = lev_sentence(input_text)
            if flag:
                mistakes += 1
            if input_text == 'exit':
                break
            else:
                rounds += 1
                intent = ds.process_sentence(input_text)
                if intent == 'exit':
                    break

    else:
        while True:
            ds.get_message()
            input_text = str(input()).lower()
            input_text = input_text.split(' ')
            if input_text == 'exit':
                break
            else:
                rounds += 1
                intent = ds.process_sentence(input_text)
                if intent == 'exit':
                    break

    print('rounds: ' + str(rounds))
    print('edits: Corrected words' + str(mistakes))

