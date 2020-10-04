#   checks if the confidence of an attribute needs to be updated according to an inference rule: if the attribute
#   does not have a value yet or has a value lower than the new confidence, the confidence of the attribute is updated
def update(list_update, attr, new_weight):
    name_list = [pair[0] for pair in list_update]
    if attr in name_list:
        pos = name_list.index(attr)
        if abs(new_weight) > abs(list_update[pos][1]):
            list_update[pos][1] = new_weight
    else: list_update.append([attr, new_weight])
    return list_update

#   input: a list of known attributes of a restaurant, and a goal attribute that needs to be checked.
def reasoning(list, goal):

    list_update = [[attr, 1] for attr in list]
    list_copy = []
    while list_update != list_copy:
        list_copy = list_update.copy()
        attr_list = [pair[0] for pair in list_update]
        if 'spanish' in attr_list:
            list_update = update(list_update, 'long time', 0.7)
        if 'cheap' in attr_list:
            list_update = update(list_update, 'romantic', -0.65)
        if 'expensive' in attr_list:
            list_update = update(list_update, 'romantic', 0.8)
        if 'expensive' in attr_list:
            list_update = update(list_update, 'good food', 0.9)
        if 'centre' in attr_list:
            list_update = update(list_update, 'busy', 0.6)
        if 'busy' in attr_list:
            list_update = update(list_update, 'long time', 0.75)
        if 'long time' in attr_list:
            list_update = update(list_update, 'late', 0.7)
        if 'cheap' in attr_list:
            list_update = update(list_update, 'busy', 0.75)
        if 'gastropub' in attr_list:
            list_update = update(list_update, 'children', -0.85)

    def goaltext(goal):
        if goal == 'long time':
            return 'suitable for spending a long time'
        elif goal == 'good food':
            return 'serving good food'
        elif goal == 'late':
            return 'open until late'
        elif goal == 'children':
            return 'suitable for children'

    if goal in attr_list:
        goal_score = list_update[attr_list.index(goal)][1]
        if goal_score > 0.5:
            print('This restaurant is probably', goaltext(goal))
        elif goal_score > 0:
            print('This restaurant might be', goaltext(goal))
        elif goal_score < -0.5:
            print('This restaurant is probably not', goaltext(goal))
        elif goal_score < 0:
            print('This restaurant might not be', goaltext(goal))
    else: print('I do not know whether this restaurant is', goaltext(goal))

reasoning(['gastropub'], 'children')
