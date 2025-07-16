import json
from datasets import load_dataset
from itertools import islice

dataset = load_dataset('ddrg/named_math_formulas', split='train', streaming=True)

start = 0
stop = 5000
subset = list(islice(dataset, start, stop))

formulas = [i['formula'] for i in subset]

# Сохраняем в JSON-файл
with open('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\data\\raw\\dataset_formulas.json', 'w', encoding='utf-8') as f:
    json.dump(formulas, f, ensure_ascii=False, indent=2)
