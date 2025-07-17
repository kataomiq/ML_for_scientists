from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


def train_model(X_train, Y_train, use_grid_search=False):
    if use_grid_search:
        param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale', 'auto'],
            'class_weight': ['balanced'],
        }

        grid = GridSearchCV(SVC(probability=True, max_iter=3000), param_grid,
                            cv=5, scoring='f1_weighted', n_jobs=-1, verbose=2)
        grid.fit(X_train, Y_train)
        print("Лучшие параметры:", grid.best_params_)
        return grid.best_estimator_

    else:
        clf = SVC(
            C=10,
            kernel='rbf',
            class_weight='balanced',
            probability=True,
            max_iter=3000
        )
        clf.fit(X_train, Y_train)
        return clf
