import pickle
from src.data_processing.Latex_processor import LatexTokenizer
from data_processing.data_preporation import labels
import numpy as np


def classify_formula(formula):
    #Загрузка модели
    with open('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\svm_model.pkl', 'rb') as f:
        clf = pickle.load(f)
    #Загрузка векторизатора
    with open('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    #Загрузка энкодера
    with open('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\models\\encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)

    tokenizer = LatexTokenizer('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\data/processed/modified_dictionary.json')
    tokens = tokenizer.tokenize(formula)
    joined = ' '.join(tokens)
    X_input = vectorizer.transform([joined])

    Y_pred = clf.predict(X_input)

    label_str = encoder.fit_transform(np.array(labels).reshape(-1, 1))

    return label_str