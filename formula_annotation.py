from yaml import tokens


def bie_annotation(tokens):
    labels = list()
    for i,  tok in enumerate(tokens):
        if tok in ['\\forall', '\\exists']:
            labels.append('B-KW')
        elif tok in ['<', '>', '=', '\\in', '\\subset']:
            labels.append('B-REL')