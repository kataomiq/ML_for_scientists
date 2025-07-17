from src.data_processing.data_preporation import load_labeled_formulas
from src.data_processing.vectorization import vectorize_formulas
from src.train_svm import train_model
from src.data_processing.split_data import split_data
from predict import classify_formula
from metrics_utils import *
import pickle


def main():
    # Загрузка формул и меток
    formulas, Y, encoder, labels = load_labeled_formulas()

    # Векторизация формул
    X, vectorizer = vectorize_formulas(formulas)

    # Делим данные
    X_train, X_test, Y_train, Y_test, train_idx, test_idx = split_data(X, Y)

    # Обучение модели
    clf = train_model(X_train, Y_train)

    # Сохраняем модель
    with open("C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\svm_model.pkl", "wb") as f:
        pickle.dump(clf, f)

    # Сохраняем векторизатор
    with open("C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    # Сохраняем энкодер
    with open("C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)

    # Предикты
    Y_pred = clf.predict(X_test)

    # Вывод метрик
    print_report_table(Y_test, Y_pred)

    show_full_classification_report(Y_test, Y_pred, labels)

    #Пользовательской ввод формулы
    '''formula = 'int_{a}^{b} f(x) dx + \sum_{ii=1}^{n}  ii + \lim_{x \to 0} f(x) \mathbb{C} i'
    predicted = classify_formula(formula)
    print('Предсказанный клласс:', predicted)'''


if __name__ == "__main__":
    main()
