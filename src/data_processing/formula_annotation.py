import json
import re
from collections import defaultdict

# Загрузка словаря
with open('../../data/processed/modified_dictionary.json', encoding='utf-8') as json_file:
    dictionary = json.load(json_file)

# Классы токенов
VAR = [s["latex"] for s in dictionary["VAR"]]
NUM = [s["latex"] for s in dictionary["NUM"]]
GEOM = [s["latex"] for s in dictionary["GEOM"]]
LOG = [s["latex"] for s in dictionary["LOG"]]
LIM = [s["latex"] for s in dictionary["LIM"]]
REP = [s["latex"] for s in dictionary["REP"]]
MAT = [s["latex"] for s in dictionary["MAT"]]
COMB = [s["latex"] for s in dictionary["COMB"]]
DIFF = [s["latex"] for s in dictionary["DIFF"]]
CONST = [s["latex"] for s in dictionary["CONST"]]
ID = [s["latex"] for s in dictionary["ID"]]
O = [s["latex"] for s in dictionary["OTHER"]]

# Пример токенов
tokens = ['\\frac', '{', 'd', '}', '{', 'd', 'x', '}', '\\le', 'f', 't', '(', '\\int', '_', '{', 'a', '}', '^', '{', 'x', '}', 'f', '(', 't', ')', '\\', ',', 'd', 't', '\\', 'r', 'i', 'g', 'h', 't', ')', '=', 'f', '(', 'x', ')']

# Паттерны для сложных операций
DIFF_PATTERNS = [
    ['\\frac', '{', 'd', '}', '{', 'd', 'x', '}'],  # \frac{d}{dx}
    ['\\int', '_', '{', 'a', '}', '^', '{', 'x', '}']  # \int_a^x
]


# Заменим паттерны единым токеном DIFF_PATTERN
def replace_diff_patterns(tokens):
    i = 0
    new_tokens = []
    while i < len(tokens):
        matched = False
        for pattern in DIFF_PATTERNS:
            if tokens[i:i+len(pattern)] == pattern:
                new_tokens.append('DIFF_PATTERN')
                i += len(pattern)
                matched = True
                break
        if not matched:
            new_tokens.append(tokens[i])
            i += 1
    return new_tokens

def merge_token_patterns(tokens, patterns):
    """
    Заменяет каждый паттерн в tokens на объединённую строку токенов, например:
    ['\\frac', '{', 'd', '}', '{', 'd', 'x', '}'] → ['\\frac{d}{dx}']
    """
    i = 0
    new_tokens = []
    while i < len(tokens):
        matched = False
        for pattern in patterns:
            pat_len = len(pattern)
            if tokens[i:i + pat_len] == pattern:
                # Склеиваем паттерн в одну строку
                merged = ''.join(pattern)
                new_tokens.append(merged)
                i += pat_len
                matched = True
                break
        if not matched:
            new_tokens.append(tokens[i])
            i += 1
    return new_tokens

print(merge_token_patterns(tokens, DIFF_PATTERNS))

# BIO разметка
def bio_tag_tokens(tokens):
    tags = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]

        # Производные/интегралы как единый паттерн
        if tok == 'DIFF_PATTERN':
            tags.append("B-DIFF")
            i += 1
            continue

        # Производные отдельно
        if tok in DIFF:
            tags.append("B-DIFF")
            i += 1
            # Продолжим I-DIFF до знака препинания или конца
            while i < len(tokens) and tokens[i] not in {',', ';', '=', '+', '-', ')'}:
                tags.append("I-DIFF")
                i += 1
            continue

        # Остальные complex_operations с BIO
        for category, label in [(LIM, "LIM"), (REP, "REP"), (MAT, "MAT"), (COMB, "COMB")]:
            if tok in category:
                tags.append(f"B-{label}")
                i += 1
                while i < len(tokens) and tokens[i] not in {',', ';', '=', '+', '-', ')'}:
                    tags.append(f"I-{label}")
                    i += 1
                break
        else:
            # Константа с минусом
            if tok == '-' and i + 1 < len(tokens) and tokens[i + 1] in CONST:
                tags.append("B-CONST")
                tags.append("I-CONST")
                i += 2
                continue

            # Просто константа
            if tok in CONST:
                tags.append("CONST")
                i += 1
                continue

            if tok in VAR:
                tags.append("VAR")
                i += 1
                continue

            if tok in NUM:
                tags.append("NUM")
                i += 1
                continue

            if tok in GEOM:
                tags.append("GEOM")
                i += 1
                continue

            if tok in LOG:
                tags.append("LOG")
                i += 1
                continue

            if tok in ID:
                tags.append("ID")
                i += 1
                continue

            tags.append(tok)
            i += 1

    return tags

# Группировка BIO-токенов
def group_bio_entities(tokens, tags):
    result = []
    i = 0
    while i < len(tags):
        tag = tags[i]
        token = tokens[i]

        if tag.startswith('B-'):
            entity_type = tag[2:]
            entity_tokens = [token]
            i += 1
            while i < len(tags) and tags[i] == f'I-{entity_type}':
                entity_tokens.append(tokens[i])
                i += 1
            result.append((f'{entity_type}', ' '.join(entity_tokens)))

        elif tag.startswith('I-'):
            # Если вдруг I без B, тоже собираем в отдельную группу
            entity_type = tag[2:]
            entity_tokens = [token]
            i += 1
            while i < len(tags) and tags[i] == f'I-{entity_type}':
                entity_tokens.append(tokens[i])
                i += 1
            result.append((f'{entity_type}', ' '.join(entity_tokens)))

        else:
            result.append((tag, token))
            i += 1

    return result




def group_consecutive_tags(tokens, tags):
    result = []
    if not tokens or not tags:
        return result

    current_tag = tags[0]
    current_tokens = [tokens[0]]

    for i in range(1, len(tokens)):
        if tags[i] == current_tag:
            current_tokens.append(tokens[i])
        else:
            result.append((current_tag, ''.join(current_tokens)))
            current_tag = tags[i]
            current_tokens = [tokens[i]]

    # Добавить последнюю группу
    result.append((current_tag, ''.join(current_tokens)))
    return result




# --- Основной процесс ---

tokens2 = replace_diff_patterns(tokens)
new_tokens = merge_token_patterns(tokens2, DIFF_PATTERNS)
print(new_tokens)
tags = bio_tag_tokens(tokens2)
print(tags)
grouped = group_consecutive_tags(tokens2, tags)

