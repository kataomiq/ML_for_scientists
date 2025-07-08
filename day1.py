def reverse_and_repeat(text):
    return text[::-1] * 3


def case_analysis(text):
    upper_count = len([i for i in text if i.isupper()])
    lower_count = len([i for i in text if i.islower()])
    title_text = text.title()

    return upper_count, lower_count, title_text


def simple_encrypt(text, key):
    result = ''
    for i in text:
        if i.isupper():
            shifted = chr((ord(i) - ord('A') + key) % 26 + ord('A'))
            result += shifted
        elif i.islower():
            shifted = chr((ord(i) - ord('a') + key) % 26 + ord('a'))
            result += shifted
        else:
            result += i
    return result


def clean_data(data):
    if data[0] == ' ': data = data[1:]
    if data[-1] == ' ': data = data[:-1]
    data = (' '.join(data.split())).title()

    result = ''
    for i in data:
        if i.isdigit(): i = ''
        else: result += i

    return result


def compress_string(text):
    uniq = sorted(set(text))
    res = ''
    if len(text) == len(uniq):
        return text
    else:
        for i in uniq:
            res += i
            res += str(text.count(i))

        return res
