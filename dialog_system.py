import pandas as pd
from BagOfWords import get_bow_unpacked


class DialogSystem:

    def __init__(self, restaurant_data, ml_model, frequent_words):
        self.state = Welcome({})
        self.data = pd.read_csv(restaurant_data)
        self.ml_model = ml_model
        self.entities = {}
        self.entities_options = self.__get_unique_entities(self.data)
        self.frequent_words = frequent_words
        self.preferences = {}

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
        if new_state.tag == 'welcome':
            self.preferences = {}
        self.state = new_state

    def __get_intent(self, sentence):
        input_vector = get_bow_unpacked(sentence, self.frequent_words)
        return self.ml_model.predict(input_vector)

    def __update_preferences(self, entities):
        print(entities)
        for key, value in entities.items():
            self.preferences[key] = value


    def process_sentence(self, sentence):
        sentence = sentence.split(' ')
        intent = self.__get_intent(sentence)
        entities = self.__get_entities(sentence)
        self.__update_preferences(entities)
        df = None
        if self.preferences != {}:
            #self.entities = self.state.assure_entities(entities)
            df = self.__get_restaurants(pricerange=self.preferences.get('pricerange', None),
                                        area=self.preferences.get('area', None),
                                        food=self.preferences.get('food', None),
                                        postcode=self.preferences.get('postcode', None))
        self.__transition(self.state.get_next_state(intent, self.preferences, df))

        return intent

    def get_message(self):
        self.state.print_message()


class State:
    states_dict: {}
    message: {}
    preferences: {}
    tag: str

    def get_next_state(self, intent, preferences_user, df):
        if df is None:
            df = []
        next_state = None
        for key, val in self.states_dict.items():
            if intent in val:
                next_state = key
        print(next_state)
        if next_state == 'End':
            exit(code=0)
        elif next_state == 'Welcome':
            return Welcome(preferences_user)
        elif next_state == 'repeat':
            print('Can you repeat please?')
            return self
        elif next_state == 'Finish':
            return Finish(preferences_user)
        elif len(df) < 3:
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                print('we only have this match for your preferences')
                print(df)
            return ChangePreferences(preferences_user)
        elif next_state == 'Preferences':
            return Preferences(preferences_user)
        else:
            return Repeat(preferences_user)

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


class Welcome(State):
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'hello'], 'repeat': ['null']}
        self.message = 'Hello, how can I help you?'
        self.preferences = preferences_user
        self.tag = 'welcome'


class Preferences(State):

    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform'],'repeat': ['null']}
        self.message = {'first' : 'Can you tell me what you are looking for?',
                        'missing_price' : 'What price range are you looking for?',
                        'missing_location': 'Where do you want to find a restaurant?',
                        'missing_food': 'What type of food would you like?'}
        self.preferences =preferences_user
        self.tag = 'preferences'

    def print_message(self):
        if self.preferences == {}:
            print(self.message['first'])
        else:
            if 'pricerange' not in self.preferences.keys():
                print(self.message['missing_price'])
            elif 'food' not in self.preferences.keys():
                print(self.message['missing_food'])
            elif 'area'not in self.preferences.keys() and 'postcode' not in self.preferences.keys():
                print(self.message['missing_location'])
            else:
                self.states_dict = {'Finish': ['inform']}


class ChangePreferences(State):
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'affirm'], 'Finish': ['negate'], 'repeat': ['null']}
        self.message = 'Do you want to change any preference? If yes tell me, or else say no'
        self.preferences = preferences_user
        self.tag = 'change_preferences'


class Repeat(State):
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform'], 'repeat': []}
        self.message = 'Can you repeat?'
        self.preferences =preferences_user
        self.tag = 'repeat'


class Finish(State):
    def __init__(self, preferences_user):
        self.states_dict = {'Welcome': ['affirm'],  'End': ['negate'], 'repeat': ['null']}
        self.message = 'Thank you, do you need anything else?'
        self.preferences = preferences_user
        self.tag = 'finish'


