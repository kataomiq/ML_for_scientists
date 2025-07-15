import json
import pandas as pd
import formmula_tokenization


class LatexProcessor:
    def __init__(self, tokenizer, json_path='enhanced_dictionary.json'):
        """
        Инициализация процессора
        :param tokenizer: экземпляр formmula_tokenization
        :param json_path: путь к файлу с расширенным словарём
        """
        self.tokenizer = tokenizer

        # Загрузка расширенного словаря
        with open(json_path, 'r', encoding='utf-8') as f:
            self.enhanced_dict = json.load(f)

        # Построение отображения категорий
        self.category_map = {}
        self.predefined_categories = []
        self._build_category_map()

        # Отображение специальных меток
        self.special_mapping = {
            '<VAR>': 'VAR',
            '<NUM>': 'CONST'
        }

        # Категории, для которых нужно обрабатывать верхние и нижние индексы
        self.diff_categories = {'LIM', 'REP', 'DIFF'}

    def _build_category_map(self):
        """Построение отображения категорий из JSON-словаря"""
        # Сбор всех категорий
        self.predefined_categories = list(self.enhanced_dict.keys())

        # Создание отображения latex → категория
        for category, items in self.enhanced_dict.items():
            for item in items:
                latex = item['latex']
                self.category_map[latex] = category

    def process(self, s):
        """
        Обработка входной строки: токенизация, приведение к категориям, обработка DIFF-структур
        :param s: входная строка
        :return: список токенов или их категорий
        """
        # Шаг 1: токенизация
        tokens = self.tokenizer.encode(s)

        # Шаг 2: приведение к категориям
        enhanced = []
        for token in tokens:
            # Обработка специальных меток
            if token in self.special_mapping:
                enhanced.append(self.special_mapping[token])
                continue

            # Поиск категории токена
            category = self.category_map.get(token)

            if category:
                # Если категория найдена
                enhanced.append(category)
            else:
                # Неизвестный токен — оставить без изменений
                enhanced.append(token)

        # Шаг 3: обработка DIFF-структур
        return self._process_diff_structures(enhanced)

    def _process_diff_structures(self, tokens):
        """
        Обработка DIFF-структур: поиск и пропуск верхних/нижних индексов
        :param tokens: список токенов после категоризации
        :return: обновлённый список токенов
        """
        result = []
        i = 0
        n = len(tokens)

        while i < n:
            # Проверка на DIFF-категории
            if tokens[i] in self.diff_categories:
                result.append(tokens[i])
                i += 1

                # Обработка верхнего и нижнего индекса
                i = self._process_subsup(tokens, i)
            else:
                result.append(tokens[i])
                i += 1

        return result

    def _process_subsup(self, tokens, i):
        """
        Обработка нижнего и верхнего индекса после DIFF-токена
        :param tokens: список токенов
        :param i: текущий индекс
        :return: новый индекс после пропуска индексной части
        """
        n = len(tokens)

        # Обработка нижнего индекса
        if i < n and tokens[i] == '_':
            i += 1  # пропускаем символ '_'

            # Проверка на фигурные скобки
            if i < n and tokens[i] == '{':
                i = self._skip_braces(tokens, i)
            elif i < n:
                i += 1  # пропуск одиночного токена

        # Обработка верхнего индекса
        if i < n and tokens[i] == '^':
            i += 1  # пропускаем символ '^'

            if i < n and tokens[i] == '{':
                i = self._skip_braces(tokens, i)
            elif i < n:
                i += 1  # пропуск одиночного токена

        return i

    def _skip_braces(self, tokens, i):
        """
        Пропуск содержимого внутри фигурных скобок
        :param tokens: список токенов
        :param i: индекс открывающей скобки
        :return: индекс после закрывающей скобки
        """
        n = len(tokens)
        brace_count = 1
        i += 1  # пропустить открывающую скобку

        while i < n and brace_count > 0:
            if tokens[i] == '{':
                brace_count += 1
            elif tokens[i] == '}':
                brace_count -= 1
            i += 1

        return i

    def export_category_dict(self):
        """
        Экспорт словаря категорий в DataFrame
        :return: DataFrame с токенами и их категориями
        """
        dict_list = []

        # Добавление специальных меток
        dict_list.append({"token": "<VAR>", "category": "VAR"})
        dict_list.append({"token": "<NUM>", "category": "CONST"})

        # Добавление обычных токенов
        for token, category in self.category_map.items():
            dict_list.append({"token": token, "category": category})

        return pd.DataFrame(dict_list)


# Пример использования
if __name__ == "__main__":
    # Инициализация токенизатора
    tokenizer = formmula_tokenization('cleaned_dictionary.json')

    # Инициализация процессора
    processor = LatexProcessor(tokenizer, '../../data/processed/modified_dictionary.json')

    test_case = r"\int_{a}^{b} f(x) dx + \sum_{ii=1}^{n} ii + \lim_{x \to 0} f(x) \mathbb{C} ii"

    # Обработка входной строки
    processed = processor.process(test_case)

    print("Оригинальный ввод:", test_case)
    print("Результат обработки:", processed)

    # Экспорт словаря категорий
    df = processor.export_category_dict()
    print("\nСловарь категорий:")
    print(df.head())
