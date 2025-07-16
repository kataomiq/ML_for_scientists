from sklearn.model_selection import train_test_split
import numpy as np


def split_data(X, Y, test_size=0.8, seed=100):
    indices = np.arange(X.shape[0])
    X_train, X_test, Y_train, Y_test, train_idx, test_idx = train_test_split(
        X, Y, indices, test_size=test_size, random_state=seed
    )

    Y_train = Y_train.toarray()
    Y_train = np.argmax(Y_train, axis=1)

    Y_test = Y_test.toarray()
    Y_test = np.argmax(Y_test, axis=1)

    return X_train, X_test, Y_train, Y_test, train_idx, test_idx
