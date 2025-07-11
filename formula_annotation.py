import json

with open('modified_dictionary.json', encoding='utf-8') as json_file:
    dictionary = json.load(json_file)

VAR = [symbol["latex"] for symbol in dictionary["VAR"]]

NUM = [symbol['latex'] for symbol in dictionary["NUM"]]
GEOM = [symbol['latex'] for symbol in dictionary["GEOM"]]
LOG = [symbol['latex'] for symbol in dictionary["LOG"]]

LIM = [symbol['latex'] for symbol in dictionary["LIM"]]
REP = [symbol['latex'] for symbol in dictionary["REP"]]
MAT = [symbol['latex'] for symbol in dictionary["MAT"]]
COMB = [symbol['latex'] for symbol in dictionary["COMB"]]
DIFF = [symbol['latex'] for symbol in dictionary["DIFF"]]

CONST = [symbol['latex'] for symbol in dictionary["CONST"]]

ID = [symbol['latex'] for symbol in dictionary["ID"]]

O = [symbol['latex'] for symbol in dictionary["OTHER"]]

tokens = ['\\frac', '{', '(', '-', '5', ')', '\\cdot', '\\frac', '{', '1', '}', '{', '4', '}',
          '}', '{', '3', '\\cdot', '1', '/', '5', '}', '=', '-', '\\frac', '{', '5', '}', '{', '4', '}', '\\cdot', '5', '/', '3']

def BIO_annotation(tokens):
    labels = list()
    for token in tokens:
        if token in VAR:
            labels.append("VAR")
        elif token in NUM:
            labels.append("NUM")
        elif token in GEOM:
            labels.append("GEO")
        elif token in LOG:
            labels.append("LOG")
        elif token in LIM:
            labels.append("LIM")
        elif token in REP:
            labels.append("REP")
        elif token in MAT:
            labels.append("MAT")
        elif token in COMB:
            labels.append("COMB")
        elif token in DIFF:
            labels.append("DIFF")
        elif token in CONST:
            labels.append("CONST")
        elif token in ID:
            labels.append("ID")
        else:
            labels.append("O")

    return labels

labels = BIO_annotation(tokens)
print(labels)

def annotation_rules(labels):
    pass



