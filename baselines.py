import json


class BaselineBasic:

    def __init__(self, data_y):
        data = []
        for i in range(len(data_y)):
            data.append(data_y[i][0])
        self.most_repeated = max(data, key=data.count)

    def predict(self):
        return self.most_repeated


class BaselineRuleBased:

    def __init__(self, data_y=None):
        with open('rules.json') as json_file:
            self.rules = json.load(json_file).get('rules')
            if data_y is not None:
                bb = BaselineBasic(data_y)
                self.base_case = bb.predict()
            else:
                self.base_case = None

    def predict(self, data_x):
        data_x = data_x.split()
        print(data_x)
        for i in range(len(data_x)):
            for key, val in self.rules.items():
                if data_x[i] in val:
                    return key

        return self.base_case
