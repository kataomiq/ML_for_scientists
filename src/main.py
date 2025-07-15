from src.data_processing.data_preporation import load_labeled_formulas
from src.data_processing.vectorization import vectorize_formulas
from src.train_svm import train_model
from src.data_processing.split_data import split_data
from metrics_utils import print_report_table

# Шаг 1: Загрузить формулы и метки
formulas, Y, encoder = load_labeled_formulas()

# Шаг 2: Векторизовать формулы
X, vectorizer = vectorize_formulas(formulas)

# Шаг 3: Разделить данные
X_train, X_test, Y_train, Y_test, train_idx, test_idx = split_data(X, Y)

# Шаг 4: Обучить модель
clf = train_model(X_train, Y_train)

# Шаг 5: Предсказать
Y_pred = clf.predict(X_test)

# Шаг 6: Метрики
print_report_table(Y_test, Y_pred)
