import pandas as pd
from BagOfWords import get_bow_unpacked


class DialogSystem:

    def __init__(self, restaurant_data, ml_model, frequent_words):
        self.state = "welcome"
        self.data = pd.read_csv(restaurant_data)
        self.ml_model = ml_model
        self.entities_options = self.__get_unique_entities(self.data)
        self.frequent_words = frequent_words

    def __get_restaurants(self, restaurantname=None,pricerange=None,area=None,food=None,phone=None,addr=None,postcode=None):
        dataframe = self.data
        if restaurantname is not None:
            dataframe = dataframe[dataframe['restaurantname'] == restaurantname]
        if pricerange is not None:
            dataframe = dataframe[dataframe['pricerange'] == pricerange]
        if area is not None:
            dataframe = dataframe[dataframe['area'] == area]
        if food is not None:
            dataframe = dataframe[dataframe['food'] == food]
        if phone is not None:
            dataframe = dataframe[dataframe['phone'] == phone]
        if addr is not None:
            dataframe = dataframe[dataframe['addr'] == addr]
        if postcode is not None:
            dataframe = dataframe[dataframe['postcode'] == postcode]
        return dataframe

    def __get_unique_entities(self, data):
        field_list = ['pricerange', 'area', 'food', 'postcode']
        field_dict = {}
        for field in field_list:
            field_dict[field] = data[field].unique()
        return field_dict

    def __get_entities(self, sentence):
        entities = {}
        for word in sentence:
            for key, value in self.entities_options.items():
                if word in value:
                    entities[key] = word
        return entities

    def __transition(self, new_state):
        self.state = new_state

    def __get_intent(self, sentence):
        input_vector = get_bow_unpacked(sentence, self.frequent_words)
        return self.ml_model.predict(input_vector)

    def process_sentence(self, sentence):
        sentence = sentence.split(' ')
        intent = self.__get_intent(sentence)
        entities = self.__get_entities(sentence)
        df = self.__get_restaurants(pricerange=entities.get('pricerange', None),
                                    area=entities.get('area', None),
                                    food=entities.get('food', None),
                                    postcode=entities.get('postcode', None))

        return df, intent


