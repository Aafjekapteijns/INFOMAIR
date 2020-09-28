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

    def get_next_state(self, intent, preferences_user, df):
        """This function is a generic function for all the states to change state, it depends on the features of every
        class inheriting from State."""
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

    def print_message(self):
        """This function prints the message of every class"""
        print(self.message)


class Welcome(State):
    """State to welcome and initiate the conversation, most of the time it will advance to preferences"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'hello'], 'repeat': ['null']}
        self.message = 'Hello, how can I help you?'
        self.preferences = preferences_user
        self.tag = 'welcome'


class Preferences(State):
    """This state is the longest and it is the one in which the user can set their preferences when it comes to finding
    a restaurant. It has various messages in case some preferences are missing, in order to create a more accurate
    search"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform'],'repeat': ['null']}
        self.message = {'first' : 'Can you tell me what you are looking for?',
                        'missing_price' : 'What price range are you looking for?',
                        'missing_location': 'Where do you want to find a restaurant?',
                        'missing_food': 'What type of food would you like?'}
        self.preferences =preferences_user
        self.tag = 'preferences'

    def print_message(self):
        """Preferences has a custom print message function in order to handle missing information in the preferences"""
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
    """This State Class is used when all the preferences have been used but the user wants to change some of them in
    order to find a different restaurant from the offered ones"""
    def __init__(self, preferences_user):
        self.states_dict = {'Preferences': ['inform', 'affirm'], 'Finish': ['negate'], 'repeat': ['null']}
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
        self.states_dict = {'Welcome': ['affirm'],  'End': ['negate'], 'repeat': ['null']}
        self.message = 'Thank you, do you need anything else?'
        self.preferences = preferences_user
        self.tag = 'finish'


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

    def __get_unique_entities(self):
        """This function gets the a dictionary of the unique options in the dataset for every feature"""
        field_list = ['pricerange', 'area', 'food', 'postcode']
        field_dict = {}
        for field in field_list:
            field_dict[field] = self.data[field].unique()
        self.entities_options = field_dict

    def __get_entities(self, sentence: str):
        """This function gets all the entities from a given sentence looking in the unique dictionary"""
        entities = {}
        for word in sentence:
            for key, value in self.entities_options.items():
                if word in value:
                    entities[key] = word
        return entities

    def __transition(self, new_state: State):
        """This function makes a transition between states of the flow"""
        if new_state.tag == 'welcome':
            self.preferences = {}
        self.state = new_state

    def __get_intent(self, sentence: str):
        """This function gets the intent of a given sentence"""
        input_vector = get_bow_unpacked(sentence, self.frequent_words)
        return self.ml_model.predict(input_vector)

    def __update_preferences(self, entities: {}):
        """This function updates the preferences of the user with new given entities"""
        print(entities)
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
            #self.entities = self.state.assure_entities(entities)
            df = self.__get_restaurants(pricerange=self.preferences.get('pricerange', None),
                                        area=self.preferences.get('area', None),
                                        food=self.preferences.get('food', None),
                                        postcode=self.preferences.get('postcode', None))
        self.__transition(self.state.get_next_state(intent, self.preferences, df))

        return intent

    def get_message(self):
        """This function calls the function of state to print a message of a specific state."""
        self.state.print_message()


