from sklearn import model_selection
import nltk
import heapq
import numpy as np


words = ["expensive", "cheap", "moderate", "south", "north", "east","west","centre", "address", "phone", "telephone",
         "thai","chinese", "korean", "vietnamese", "asian oriental",
         "mediterranean", "spanish", "portuguese", "italian", "romanian", "tuscan", "catalan",
         "french", "european", "bistro", "swiss", "gastropub", "traditional",
         "north american", "steakhouse", "british",
         "lebanese", "turkish", "persian", "want",
         "international", "modern european", "fusion"]


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


def get_word_freq(contents):
    wordfreq = {}
    for content in contents:
        tokens = nltk.word_tokenize(content[0])
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1
    most_freq = heapq.nlargest(700, wordfreq, key=wordfreq.get)

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



def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1 - 1] == token2[t2 - 1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def lev_distance(word:str, numwords: int = 3):
    dictWordDist = []
    wordIdx = 0

    for line in words:
        wordDistance = levenshteinDistanceDP(word, line)
        if wordDistance >= 10:
            wordDistance = 9
        dictWordDist.append(str(int(wordDistance)) + "-" + line)
        wordIdx = wordIdx + 1

    closestWords = []
    wordDetails = []
    currWordDist = 0
    dictWordDist.sort()

    for i in range(1):
        currWordDist = dictWordDist[i]
        wordDetails = currWordDist.split("-")
        closestWords.append(wordDetails[1])
        if int(wordDetails[0]) < 3:
            return wordDetails[1]
    return word


def lev_sentence(sentence):
    sentence = sentence.split(' ')
    words_lev = []
    for word in sentence:
        words_lev.append(lev_distance(word))
    return words_lev
