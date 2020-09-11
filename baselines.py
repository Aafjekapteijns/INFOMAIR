import numpy as np
import json


class BaselineBasic:

    def __init__(self, data_y):
        self.most_repeated = np.bincount(data_y).argmax()

    def get_classification(self):
        return self.most_repeated


class BaselineRuleBased:

    def __init__(self):
        with open('rules.json') as json_file:
            self.rules = json.load(json_file).get('rules')

    def get_classification(self, data_x):
        data_x = data_x[0].split()
        print(data_x)
        for i in range(len(data_x)):
            for key, val in self.rules.items():
                if data_x[i] in val:
                    return key
        return None
