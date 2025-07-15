import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer  # Преобразует формулы в векторы по TF-IDF
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split  # нужно, чтобы разделить данные на тест и обчуение
from sklearn.preprocessing import OneHotEncoder

from data.raw.formulas import *
from metrics_utils import *
from src.data_processing.formmula_tokenization import LatexTokenizer

all_formulas = (set_logic_formulas + type_geometry + formulas_probability_combo
                + differential_eq_formulas + algebra_formulas + calculus_formulas)

labels = ['LOG', 'GEO',
          'COMB', 'DIFF',
          'ALG', 'CALC']

formula_labels = (['LOG'] * len(set_logic_formulas) + ['GEO'] * len(type_geometry)
                  + ['COMB'] * len(formulas_probability_combo) + ['DIFF'] * len(differential_eq_formulas)
                  + ['ALG'] * len(algebra_formulas)  + ['CALC'] * len(calculus_formulas))

labels_array = np.array(labels).reshape(-1, len(labels))

encoder = OneHotEncoder()
onehot_labels = encoder.fit_transform(labels_array)
label_vectors = encoder.fit_transform(np.array(formula_labels).reshape(-1, 1))

"""print(onehot_labels)"""

tokenizer = LatexTokenizer('../data/processed/cleaned_dictionary.json')

def custom_tokenizer(formula):
    return tokenizer.tokenize(formula)

vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
X = vectorizer.fit_transform(all_formulas) #разряженая матрица
Y = label_vectors

"""print("Форма матрицы TF-IDF:", X.shape)
print("Пример токенов:", custom_tokenizer(all_formulas[0]))
print("Словарь признаков:", vectorizer.get_feature_names_out())

for i, formula in enumerate(all_formulas):
    print(f"Формула {i + 1}: {formula}")
    vector = X[i].toarray()[0]
    tfidf_tokens = [(token, vector[j]) for j, token in enumerate(vectorizer.get_feature_names_out()) if vector[j] > 0]
    print("TF-IDF токены:", tfidf_tokens)
    print("-" * 80)

dense_matrix = X.toarray()
print(dense_matrix)"""

indices = np.arange(len(all_formulas))
X_train, X_test, Y_train, Y_test, train_idx, test_idx = train_test_split(
    X, Y, indices, test_size=0.2, random_state=400)

Y_train = Y_train.toarray()
Y_train = np.argmax(Y_train, axis=1)

Y_test = Y_test.toarray()
Y_test = np.argmax(Y_test, axis=1)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, Y_train)

Y_pred = clf.predict(X_test)


"""
class_names = encoder.categories_[0]

for idx, true_label_num, pred_label_num in zip(test_idx, Y_test, Y_pred):
    formula = all_formulas[idx]
    true_label = class_names[true_label_num]
    pred_label = class_names[pred_label_num]
    print(f"Формула: {formula}")
    print(f"Истинный класс: {true_label}, Предсказанный класс: {pred_label}")
    print('-' * 40)
"""

print_report_table(Y_test, Y_pred)
