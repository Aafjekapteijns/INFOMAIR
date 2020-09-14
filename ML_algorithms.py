from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree, metrics
import pandas as pd


def train_logistic_regresor(x_train, y_train):
    logistic_regr = LogisticRegression()
    logistic_regr.fit(x_train, y_train)

    return logistic_regr


def train_gaussian_nb(x_train, y_train):
    gnb = GaussianNB()
    gnb.fit(x_train, y_train.ravel())

    return gnb


def train_multinomial_nb(x_train, y_train):
    mnb = MultinomialNB()
    mnb.fit(x_train, y_train.ravel())

    return mnb


def train_decision_tree(x_train, y_train):
    estimator = tree.DecisionTreeClassifier(random_state=0)
    param_distributions = {"max_depth": [x for x in range(1, 1000)], "min_samples_split": [x for x in range(2, 1000)],
                           "min_samples_leaf": [x for x in range(1, 1000)],
                           "max_leaf_nodes": [x for x in range(2, 1000)]}
    n_iter = 500
    scoring = ["accuracy"]
    cv = StratifiedKFold(n_splits=2)
    refit = "accuracy"

    randomized_search_tree = RandomizedSearchCV(estimator=estimator,
                                                param_distributions=param_distributions, n_iter=n_iter,
                                                scoring=scoring, cv=cv, refit=refit, random_state=0)

    search_tree = randomized_search_tree.fit(x_train, y_train)
    results_tree = pd.DataFrame(search_tree.cv_results_)

    best_params = search_tree.best_params_
    best_decision_tree = search_tree.best_estimator_

    return best_decision_tree


def train_sktree(x_train, y_train):
    decision_tree = tree.DecisionTreeClassifier(random_state=0)
    decision_tree.fit(x_train, y_train)

    return decision_tree


def print_results(y_test, y_pred):
    print(metrics.classification_report(y_test, y_pred))
