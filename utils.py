from sklearn import model_selection
import nltk
import heapq
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


def reasoning(list_in):
    list_update = list_in
    list_copy = []
    while list_update != list_copy:
        list_copy = list_update.copy()
        if 'spanish' in list_in and 'long time' not in list_in:
            list_update.append('long time')
        if 'cheap' in list_in and 'not romantic' not in list_in:
           list_update.append('not romantic')
        if 'expensive' in list_in and 'romantic' not in list_in:
            list_update.append('romantic')
        if 'expensive' in list_in and 'good food' not in list_in:
            list_update.append('good food')
        if 'centre' in list_in and 'busy' not in list_in:
            list_update.append('busy')
        if 'busy' in list_in and 'late' not in list_in:
            list_update.append('late')
        if 'long time' in list_in and 'late' not in list_in:
            list_update.append('late')
        if 'cheap' in list_in and 'good food' in list_in and 'busy' not in list_in:
            list_update.append('busy')
        if 'gastropub' in list_in and 'not children' not in list_in:
            list_update.append('not children')
    return list_update


def get_word_freq(contents):
    wordfreq = {}
    for content in contents:
        tokens = nltk.word_tokenize(content[0])
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1
    most_freq = heapq.nlargest(200, wordfreq, key=wordfreq.get)

    return most_freq


def get_bow(contents, most_freq):
    content_vectors = []
    for content in contents:
        content_tokens = nltk.word_tokenize(content[0])
        sent_vec = []
        for token in most_freq:
            if token in content_tokens:
                sent_vec.append(1)
            else:
                sent_vec.append(0)
        content_vectors.append(sent_vec)

    return content_vectors


def get_bow_unpacked(contents, most_freq):
    content_vectors = np.zeros(len(most_freq))
    for content in contents:
        content_tokens = nltk.word_tokenize(content)
        for i in range(len(most_freq)):
            if most_freq[i] in content_tokens:
                content_vectors[i] = 1

    return [content_vectors]
