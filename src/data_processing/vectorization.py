from sklearn.feature_extraction.text import TfidfVectorizer
from src.data_processing.formmula_tokenization import LatexTokenizer
from src.data_processing.data_preporation import *
from sklearn.preprocessing import OneHotEncoder
import numpy as np


def vectorize_formulas(formulas):
    """
    Преобразует список формул в матрицу TF-IDF признаков с использованием кастомного токенизатора.

    :param formulas: список строк — формулы
    :param tokenizer_path: путь к JSON-файлу с токенами
    :return: X — разреженная матрица признаков, vectorizer — обученный TfidfVectorizer
    """
    tokenizer = LatexTokenizer('../data/processed/cleaned_dictionary.json')

    def custom_tokenizer(formula):
        return tokenizer.tokenize(formula)

    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
    X = vectorizer.fit_transform(formulas)

    return X, vectorizer


def vectorize_labels(labels):
    encoder = OneHotEncoder()
    vectors = encoder.fit_transform(np.array(labels).reshape(-1, 1))
    return vectors, encoder