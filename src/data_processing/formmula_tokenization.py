import json
import re
import pandas as pd

class LatexTokenizer:
    def __init__(self, json_path='C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\data\\processed\\cleaned_dictionary.json'):
        """
        Инициализация токенизатора
        :param json_path: путь к JSON-файлу словаря
        """
        # Загрузка данных словаря
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Построение отображений
        self._build_mappings()

    def _build_mappings(self):
        self.latex_category_map = {}
        self.char_category_map = {}

        for category, entries in self.data.items():
            for entry in entries:
                latex = entry.get('latex')
                char = entry.get('char')
                if latex is not None:
                    self.latex_category_map[latex] = category
                if char is not None:
                    self.char_category_map[char] = category

        # Теперь сформируем множества для цифр и переменных из соответствующих категорий:
        self.number_chars = {entry['char'] for entry in self.data.get('NUM', []) if
                             'char' in entry and entry['char'].isdigit()}
        self.var_chars = {entry['char'] for entry in self.data.get('VAR', []) if 'char' in entry}

        # Список LaTeX-команд отсортируем по убыванию длины
        self.latex_list = sorted(
            self.latex_category_map.keys(),
            key=lambda x: (-len(x), x)
        )

    def tokenize(self, s):
        """
        Метод токенизации
        :param s: входная строка
        :return: список токенов
        """
        # Шаг 1: разбить по пробелам и удалить пустые строки
        parts = [p for p in re.split(r'\s+', s) if p]
        tokens = []

        for part in parts:
            # Шаг 2: выполнить посимвольную токенизацию каждой части
            i = 0
            while i < len(part):
                matched = False
                for latex in self.latex_list:
                    if part.startswith(latex, i):
                        tokens.append(latex)
                        i += len(latex)
                        matched = True
                        break
                if not matched:
                    tokens.append(part[i])
                    i += 1
        return tokens

    def encode(self, s):
        """
        Полный процесс кодирования
        :param s: входная строка
        :return: список закодированных токенов
        """
        tokens = self.tokenize(s)
        return self._encode_tokens(tokens)

    def _encode_tokens(self, tokens):
        encoded = []
        for token in tokens:
            category = self.latex_category_map.get(token, None)
            if category is not None:
                # Маппинг категорий в теги
                if category == 'NUM':
                    encoded.append('<NUM>')
                elif category == 'VAR':
                    encoded.append('<VAR>')
                elif category == 'CONST':
                    encoded.append('<NUM>')  # или что подходит
                else:
                    encoded.append(token)
            else:
                # одиночные символы
                if token in self.number_chars:
                    encoded.append('<NUM>')
                elif token in self.var_chars:
                    encoded.append('<VAR>')
                else:
                    encoded.append('<UNO>')
        return self._merge_continuous(encoded)

    def _merge_continuous(self, encoded):
        """Объединение подряд идущих одинаковых меток"""
        result = []
        prev = None

        for item in encoded:
            # Пропускать повторяющиеся <NUM> или <VAR>
            if item in ('<NUM>', '<VAR>') and item == prev:
                continue

            result.append(item)
            prev = item

        return result

    def decode(self, encoded):
        """
        Метод декодирования: превращает закодированные токены обратно в строку
        :param encoded: список закодированных токенов
        :return: восстановленная строка
        """
        decoded_tokens = []
        for item in encoded:
            if item == '<NUM>':
                decoded_tokens.append('0')
            elif item == '<VAR>':
                decoded_tokens.append('a')
            elif item == '<UNO>':
                decoded_tokens.append('1')
            else:
                # Сохраняем оригинальный токен
                decoded_tokens.append(item)
        return ''.join(decoded_tokens)

    def export_token_dict(self):
        """
        Генерация упрощённого словаря токенов в виде DataFrame
        Возвращает DataFrame со следующими колонками:
        - token: LaTeX-команда
        - category: соответствующая категория
        """
        dict_list = []
        for latex, category in self.latex_category_map.items():
            dict_list.append({
                "token": latex,
                "category": category
            })

        return pd.DataFrame(dict_list).sort_values('token').reset_index(drop=True)


# Пример использования
if __name__ == "__main__":
    tokenizer = LatexTokenizer()

    test_case = r"\int_{a}^{b} f(x) dx + \sum_{i=1}^{n} ii"  # Исходный ввод
    tokens = tokenizer.tokenize(test_case)
    encoded = tokenizer.encode(test_case)
    decode = tokenizer.decode(  encoded)

    print("Исходный ввод:", test_case)
    print("Результат токенизации:", tokens)
    print("Результат кодирования:", encoded)
    print("Результат декодирования:", decode)
