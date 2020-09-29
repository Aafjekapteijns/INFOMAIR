import nltk
import heapq
import numpy as np


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
