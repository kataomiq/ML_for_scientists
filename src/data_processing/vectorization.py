from sklearn.feature_extraction.text import TfidfVectorizer
from src.data_processing.Latex_processor import *
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Загружаем токенизатор один раз глобально
tokenizer = LatexTokenizer('../data/processed/modified_dictionary.json')

def custom_tokenizer(formula):
    return tokenizer.tokenize(formula)

def vectorize_formulas(formulas):
    """
    Преобразует список формул в матрицу TF-IDF признаков с использованием кастомного токенизатора.
    :param formulas: список строк — формулы
    :return: X — разреженная матрица признаков, vectorizer — обученный TfidfVectorizer
    """
    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
    X = vectorizer.fit_transform(formulas)
    return X, vectorizer

def vectorize_labels(labels):
    encoder = OneHotEncoder()
    vectors = encoder.fit_transform(np.array(labels).reshape(-1, 1))
    return vectors, encoder
