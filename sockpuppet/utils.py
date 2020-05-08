import re


def camelize(word):
    word = re.sub(
        r'[\s_](.)',
        lambda m: m.group(1).title(),
        word, flags=re.DOTALL
    )
    return word


def camelize_value(value):
    if isinstance(value, list):
        value = [camelize_value(val) for val in value]
    elif isinstance(value, dict):
        value = {camelize(key): camelize_value(val) for key, val in value.items()}
    return value


def classify(word):
    tail = camelize(word[1:])
    head = word[:1].title()
    return '{}{}'.format(head, tail)
