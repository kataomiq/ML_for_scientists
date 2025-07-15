from data.raw.formulas import *
from sklearn.preprocessing import OneHotEncoder
import numpy as np


all_formulas = (set_logic_formulas + type_geometry + formulas_probability_combo
                + differential_eq_formulas + algebra_formulas + calculus_formulas)

labels = ['LOG', 'GEO', 'COMB', 'DIFF', 'ALG', 'CALC']

formula_labels = (['LOG'] * len(set_logic_formulas) + ['GEO'] * len(type_geometry)
                  + ['COMB'] * len(formulas_probability_combo) + ['DIFF'] * len(differential_eq_formulas)
                  + ['ALG'] * len(algebra_formulas)  + ['CALC'] * len(calculus_formulas))

encoder = OneHotEncoder()
label_vectors = encoder.fit_transform(np.array(formula_labels).reshape(-1, 1))


def load_labeled_formulas():
    return all_formulas, label_vectors, encoder

