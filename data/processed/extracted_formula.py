from src.data_processing.latex_formula_extractor import extract_latex_formulas
from pathlib import Path

file_path = Path('C:\\Users\\veder\\PycharmProjects\\ML_for_scientists\\arxiv2latex\\file.tex')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

formulas = extract_latex_formulas(content)

print(f"Найдено формул: {len(formulas)}")
print(formulas)  # список формул