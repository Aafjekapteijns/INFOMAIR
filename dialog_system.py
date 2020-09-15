import pandas as pd
from BagOfWords import get_bow_unpacked


class DialogSystem:

    def __init__(self, restaurant_data, ml_model, frequent_words):
        self.state = WelcomeState()
        self.data = pd.read_csv(restaurant_data)
        self.ml_model = ml_model
        self.entities = {}
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
        if entities != {}:
            self.entities = self.state.assure_entities(entities)
            df = self.__get_restaurants(pricerange=self.entities.get('pricerange', None),
                                        area=self.entities.get('area', None),
                                        food=self.entities.get('food', None),
                                        postcode=self.entities.get('postcode', None))
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                print(df)
        self.__transition(self.state.get_next_state(intent))

        return intent

    def get_message(self):
        self.state.print_message()


class State:
    states_dict: {}
    message: str

    def get_next_state(self, intent):
        next_state = None
        for key, val in self.states_dict.items():
            if intent in val:
                next_state = key

        if next_state == 'Preferences':
            return Preferences()
        else:
            return Repeat()

    def assure_entities(self, entities):
        assured_entities = {}
        print(entities)
        for category, entity in entities.items():
            if category == 'pricerange':
                print('You want a ' + str(entity) + ' restaurant?')
                if input() == 'yes':
                    assured_entities[category] = entity
            if category == 'area':
                print('You want a restaurant in ' + str(entity) + ' area?')
                if input() == 'yes':
                    assured_entities[category] = entity

            if category == 'food':
                print('You want a ' + str(entity) + ' restaurant?')
                if input() == 'yes':
                    assured_entities[category] = entity

            if category == 'postcode':
                print('You want a restaurant in ' + str(entity) + ' postcode?')
                if input() == 'yes':
                    assured_entities[category] = entity
        return assured_entities

    def print_message(self):
        print(self.message)


class WelcomeState(State):

    def __init__(self):
        self.states_dict = {'Preferences': ['inform', 'hello'], 'repeat': []}
        self.message = 'Hello, how can I help you?'


class Preferences(State):

    def __init__(self):
        self.states_dict = {'Preferences': ['inform'], 'repeat': []}
        self.message = 'Can you tell me what you are looking for?'


class Repeat(State):
    def __init__(self):
        self.states_dict = {'Preferences': ['inform'], 'repeat': []}
        self.message = 'Can you repeat?'
