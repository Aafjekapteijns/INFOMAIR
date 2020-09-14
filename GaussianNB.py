from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
X_train_num = BagOfWords(X_train)
X_test_num = BagOfWords(X_test)
y_pred = gnb.fit(X_train_num, y_train.ravel()).predict(X_test_num)
print(len(y_test))
print(len(y_pred))
print((y_test.ravel() != y_pred).sum())
print("Accuracy: ", (y_test.ravel() != y_pred).sum()/len(y_test))