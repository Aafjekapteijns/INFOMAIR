import pandas as pd
from utils import get_bow_unpacked


class State:
    """
    This class is an abstract class that represents the state in which the dialog is in the moment, for that purpose,
    several classes inherit from State to create  the different options
    """
    states_dict: {}
    message: {}
    preferences: {}
    tag: str
    counter: int
    df: pd.DataFrame

    def get_next_state(self, intent, preferences_user, df):
        """This function is a generic function for all the states to change state, it depends on the features of every
        class inheriting from State."""
        new_state = None
        if df is None:
            df = []
        next_state = None
        for key, val in self.states_dict.items():
            if intent in val:
                next_state = key
        print(next_state)

        if next_state == 'End':
            exit(code=0)
        elif self.tag == 'ShowMultiple' and next_state == 'ShowMultiple':
            self.counter += 1
            preferences_user['restaurantname'] = self.df['restaurantname'].to_numpy()[self.counter]
            self.__print_dataframe(self.df, '1', self.counter)
            new_state = self
        elif next_state == 'ShowMultiple':
            self.__print_dataframe(df, '1', 0)
            preferences_user['restaurantname'] = df['restaurantname'].to_numpy()[0]
            new_state = ShowMultiple(preferences_user, df)
        elif next_state == 'Welcome':
            new_state = Welcome(preferences_user)
        elif next_state == 'repeat':
            print('Can you repeat please?')
            new_state = self
        elif next_state == 'Finish':
            new_state = Finish(preferences_user)
        elif next_state == 'RequestMore':
            if preferences_user['request'] == 'phone':
                self.__print_dataframe(df, 'P')
            elif preferences_user['request'] == 'address':
                self.__print_dataframe(df, 'A')
            new_state = RequestMore(preferences_user)
        elif len(df) <= 1:
            if len(df) == 0:
                print('I am sorry, we have no coincidences')
            else:
                self.__print_dataframe(df,'N')
            new_state = ChangePreferences(preferences_user)
        elif self.tag == 'welcome' and next_state == 'Preferences':
            new_state = Preferences(preferences_user)
        elif next_state == 'ChangePreferences':
            new_state = ChangePreferences(preferences_user)
        elif next_state == 'Preferences':
            new_state = Preferences(preferences_user)
        else:
            new_state = Repeat(preferences_user)

        return new_state, preferences_user

    def assure_entities(self, entities):
        """This class is made to assure the preferences of the user, currently not used but will be possible to
        activate it in the final version of the project"""
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

    def __print_dataframe(self, df, field, row=0):
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            if field == 'N':
                print('we only have this match for your preferences')
                print(df['restaurantname'].to_csv(index=False))
            elif field == 'P':
                print(df['phone'].to_csv(index=False))
            elif field == 'A':
                print(df['addr'].to_csv(index=False))
            elif field == '1':
                print(df['restaurantname'].to_numpy()[row])

    def print_message(self):
        """This function prints the message of every class"""
        print(self.message)


class Welcome(State):
    """State to welcome and initiate the conversation, most of the time it will advance to preferences"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'hello'],
                            'repeat': ['null']}
        self.message = 'Hello, how can I help you?'
        self.preferences = preferences_user
        self.tag = 'welcome'


class Preferences(State):
    """This state is the longest and it is the one in which the user can set their preferences when it comes to finding
    a restaurant. It has various messages in case some preferences are missing, in order to create a more accurate
    search"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'negate'],
                            'ShowMultiple': ['affirm'],
                            'repeat': ['null'],
                            'RequestMore': ['request']}
        self.message = {'first' : 'Can you tell me what you are looking for?',
                        'missing_price' : 'What price range are you looking for? [cheap, moderate or expensive]',
                        'missing_location': 'Where do you want to find a restaurant?',
                        'missing_food': 'What type of food would you like?',
                        'finish': 'Thank you, we found at least an option, would you like to see it?'}
        self.preferences = preferences_user
        self.tag = 'preferences'

    def print_message(self):
        """Preferences has a custom print message function in order to handle missing information in the preferences"""
        if self.preferences == {}:
            print(self.message['first'])
        else:
            if 'pricerange' not in self.preferences.keys():
                print(self.message['missing_price'])
                self.preferences['pricerange'] = 'all'
            elif 'food' not in self.preferences.keys():
                print(self.message['missing_food'])
                self.preferences['food'] = 'all'
            elif 'area'not in self.preferences.keys() and 'postcode' not in self.preferences.keys():
                print(self.message['missing_location'])
                self.preferences['area'] = 'all'
                self.preferences['postcode'] = 'all'
            else:
                print(self.message['finish'])


class ChangePreferences(State):
    """This State Class is used when all the preferences have been used but the user wants to change some of them in
    order to find a different restaurant from the offered ones"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'affirm'],
                            'Finish': ['negate'],
                            'repeat': ['null'],
                            'RequestMore': ['request']}
        self.message = 'Do you want to change any preference? If yes tell me, or else say no'
        self.preferences = preferences_user
        self.tag = 'change_preferences'


class Repeat(State):
    """This State Class is used when the sentence from the user was not understood and repeats the same State as before
    """
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform'], 'repeat': []}
        self.message = 'Can you repeat?'
        self.preferences =preferences_user
        self.tag = 'repeat'


class Finish(State):
    """This State Class is used when the process of looking or a restaurant is finished, therefore we offer the user the
     possibility to look for a new restaurant or exit the program"""
    def __init__(self, preferences_user):
        self.states_dict = {'Welcome': ['affirm'],
                            'End': ['negate', 'bye'],
                            'repeat': ['null'],
                            'RequestMore': ['request']}
        self.message = 'Thank you, do you need anything else?'
        self.preferences = preferences_user
        self.tag = 'finish'


class RequestMore(State):
    """This State Class is used when the user asks for the address or phone"""
    def __init__(self, preferences_user):
        self.states_dict = {'End': ['negate', 'bye'],
                            'repeat': ['null'],
                            'RequestMore': ['request']}
        self.message = 'Here it is, anything else?'
        self.preferences = preferences_user
        self.tag = 'request_more'


class ShowMultiple(State):
    def __init__(self, preferences_user, df):
        self.states_dict = {'ChangePreferences': ['negate', 'affirm'],
                            'repeat': ['null'],
                            'ShowMultiple': ['reqmore'],
                            'RequestMore': ['request']}
        self.message = {'more': 'Here is one, type more for another option',
                        'last': 'This is the last one, do you need anything else?'}
        self.counter = 0
        self.df = df
        self.preferences = preferences_user
        self.tag = 'ShowMultiple'

    def print_message(self):
        """ShowMultiple has a custom print message function in order to handle multiple options"""
        if self.counter < len(self.df)-1:
            print(self.message['more'])
        else:
            print(self.message['last'])


class DialogSystem:
    """
    This class models a complete dialog system for the restaurant chatbot, it has states to which it transitions to
    simulate the actual transitions of a normal conversation to find a restaurant. Some functions have been implemented
    in order to access the data base and retrive important information from the input text
    """

    def __init__(self, restaurant_data: str, ml_model, frequent_words):
        self.state = Welcome({})
        self.data = pd.read_csv(restaurant_data)
        self.ml_model = ml_model
        self.entities = {}
        self.__get_unique_entities()
        self.frequent_words = frequent_words
        self.preferences = {}

    def __get_restaurants(self, restaurantname: str = None, pricerange: str = None, area: str = None,
                          food: str = None, phone: str = None, addr: str = None, postcode: str = None):
        """This function gets the restaurants available in the database with the user preferences"""
        dataframe = self.data
        if restaurantname is not None and restaurantname != 'all':
            dataframe = dataframe[dataframe['restaurantname'] == restaurantname]
        if pricerange is not None and pricerange != 'all':
            dataframe = dataframe[dataframe['pricerange'] == pricerange]
        if area is not None and area != 'all':
            dataframe = dataframe[dataframe['area'] == area]
        if food is not None and food != 'all':
            dataframe = dataframe[dataframe['food'] == food]
        if phone is not None and phone != 'all':
            dataframe = dataframe[dataframe['phone'] == phone]
        if addr is not None and addr != 'all':
            dataframe = dataframe[dataframe['addr'] == addr]
        if postcode is not None and postcode != 'all':
            dataframe = dataframe[dataframe['postcode'] == postcode]
        return dataframe

    def __get_unique_entities(self):
        """This function gets the a dictionary of the unique options in the dataset for every feature"""
        field_list = ['pricerange', 'area', 'food', 'postcode']
        field_dict = {}
        for field in field_list:
            field_dict[field] = self.data[field].unique()
        field_dict['request'] = ['phone', 'address']
        self.entities_options = field_dict

    def __get_entities(self, sentence: str):
        """This function gets all the entities from a given sentence looking in the unique dictionary"""
        entities = {}
        for word in sentence:
            for key, value in self.entities_options.items():
                if word in value:
                    entities[key] = word
        return entities

    def __transition(self, new_state: State, preferences):
        """This function makes a transition between states of the flow"""
        if new_state.tag == 'welcome':
            self.preferences = {}
        self.state = new_state
        self.preferences = preferences

    def __get_intent(self, sentence: str):
        """This function gets the intent of a given sentence"""
        input_vector = get_bow_unpacked(sentence, self.frequent_words)
        return self.ml_model.predict(input_vector)

    def __update_preferences(self, entities: {}):
        """This function updates the preferences of the user with new given entities"""
        for key, value in entities.items():
            self.preferences[key] = value

    def process_sentence(self, sentence: str):
        """
        This function process the sentence running multiple of the previous functions in order to extract the
        entities, the intent and  update the user preferences. It creates a dataframe with the available restaurants and
        assures that the state transition is done."""
        sentence = sentence.split(' ')
        intent = self.__get_intent(sentence)
        entities = self.__get_entities(sentence)
        self.__update_preferences(entities)
        df = None
        if self.preferences != {}:
            df = self.__get_restaurants(restaurantname=self.preferences.get('restaurantname',None),
                                        pricerange=self.preferences.get('pricerange', None),
                                        area=self.preferences.get('area', None),
                                        food=self.preferences.get('food', None),
                                        postcode=self.preferences.get('postcode', None))
        state, preferences = self.state.get_next_state(intent, self.preferences, df)
        self.__transition(state, preferences)

        return intent

    def get_message(self):
        """This function calls the function of state to print a message of a specific state."""
        self.state.print_message()


