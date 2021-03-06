import pandas as pd


def update(list_update, attr, new_weight):
    """This function updates the confidence weight of an attribute, or adds it to the list if it is new"""
    name_list = [pair[0] for pair in list_update]
    if attr in name_list:
        pos = name_list.index(attr)
        if abs(new_weight) > abs(list_update[pos][1]):
            list_update[pos][1] = new_weight
    else: list_update.append([attr, new_weight])
    return list_update


def inference(list):
    """This function iteratively applies inference rules to the list of attributes until it has found all consequences"""

    list_update = [[attr, 1] for attr in list]
    list_copy = []

    while list_update != list_copy:
        list_copy = list_update.copy()
        attr_list = [pair[0] for pair in list_update]
        if 'cheap' in attr_list and 'good food' in attr_list:
            list_update = update(list_update, 'busy', 0.8)
        if 'spanish' in attr_list:
            list_update = update(list_update, 'long_time', 0.7)
        if 'busy' in attr_list:
            list_update = update(list_update, 'long_time', 0.6)
        if 'long time' in attr_list:
            list_update = update(list_update, 'children', -0.7)
        if 'busy' in attr_list:
            list_update = update(list_update, 'romantic', -0.75)
        if 'long time' in attr_list:
            list_update = update(list_update, 'romantic', 0.6)

        if 'cheap' in attr_list:
            list_update = update(list_update, 'romantic', -0.65)
        if 'expensive' in attr_list:
            list_update = update(list_update, 'romantic', 0.8)
        if 'busy' in attr_list:
            list_update = update(list_update, 'large_groups', -0.65)
        if 'centre' in attr_list:
            list_update = update(list_update, 'busy', 0.6)
        if 'busy' in attr_list:
            list_update = update(list_update, 'long_time', 0.75)
        if 'long_time' in attr_list:
            list_update = update(list_update, 'late', 0.7)
        if 'cheap' in attr_list:
            list_update = update(list_update, 'busy', 0.75)
        if 'gastropub' in attr_list:
            list_update = update(list_update, 'children', -0.85)
    return list_update


def goaltext(goal):
    """This function assigns specific text to certain properties so it can be presented to the user"""
    if goal == 'long_time':
        return 'suitable for spending a long time'
    elif goal == 'large groups':
        return 'suitable for large groups'
    elif goal == 'late':
        return 'open until late'
    elif goal == 'children':
        return 'suitable for children'
    else: return goal

'''if goal in attr_list:
    goal_score = list_update[attr_list.index(goal)][1]
    if goal_score > 0.5:
        print('This restaurant is probably', goaltext(goal))
    elif goal_score > 0:
        print('This restaurant might be', goaltext(goal))
    elif goal_score < -0.5:
        print('This restaurant is probably not', goaltext(goal))
    elif goal_score < 0:
        print('This restaurant might not be', goaltext(goal))
else:
    print('I do not know whether this restaurant is', goaltext(goal))
'''


def rest_inf():
    rests = pd.read_csv('restaurants_info.csv')
    rests["busy"] = 0
    rests["long_time"] = 0
    rests["late"] = 0
    rests["romantic"] = 0
    rests["children"] = 0
    rests["large_groups"] = 0
    for i in range(len(rests)):
        attrs = rests.iloc[i, 1:4].tolist()
        attrs_up = inference(attrs)
        for item in attrs_up:
            if item[0] == 'busy':
                rests.iloc[i, 7] = item[1]
            elif item[0] == 'long_time':
                rests.iloc[i, 8] = item[1]
            elif item[0] == 'late':
                rests.iloc[i, 9] = item[1]
            elif item[0] == 'romantic':
                rests.iloc[i, 10] = item[1]
            elif item[0] == 'children':
                rests.iloc[i, 11] = item[1]
            elif item[0] == 'large_groups':
                rests.iloc[i, 7] = item[1]
    return rests


def rest_inf2(rests):
    rests["busy"] = 0
    rests["long_time"] = 0
    rests["late"] = 0
    rests["romantic"] = 0
    rests["children"] = 0
    rests["large_groups"] = 0
    for i in range(len(rests)):
        attrs = rests.iloc[i, 1:4].tolist()
        attrs_up = inference(attrs)
        for item in attrs_up:
            if item[0] == 'busy':
                rests.iloc[i, 7] = item[1]
            elif item[0] == 'long_time':
                rests.iloc[i, 8] = item[1]
            elif item[0] == 'late':
                rests.iloc[i, 9] = item[1]
            elif item[0] == 'romantic':
                rests.iloc[i, 10] = item[1]
            elif item[0] == 'children':
                rests.iloc[i, 11] = item[1]
            elif item[0] == 'large_groups':
                rests.iloc[i, 7] = item[1]
    return rests
