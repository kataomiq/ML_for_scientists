from sklearn.linear_model import LogisticRegression


def train_model(X_train, Y_train, max_iter=1000):
    clf = LogisticRegression(max_iter=max_iter)
    clf.fit(X_train, Y_train)
    return clf
