from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
mnb = MultinomialNB()
freq = get_word_freq(X_train)
X_train_num = get_bow(X_train, freq)
X_test_num = get_bow(X_test, freq)
y_pred = mnb.fit(X_train_num, y_train.ravel()).predict(X_test_num)
report = metrics.classification_report(y_test.ravel(), y_pred)
print(report)
