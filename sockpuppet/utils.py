from inflector import Inflector

inflector = Inflector()


def camelize(word):
    word = inflector.camelize(word)
    return '{}{}'.format(word[0].lower(), word[1:])


def classify(word):
    tail = camelize(word[1:])
    head = word[:1].title()
    return '{}{}'.format(head, tail)


def deep_transform(obj, transform_function):
    """ Deeply transform keys """
    if isinstance(obj, dict):
        return {
            transform_function(k): deep_transform(v, transform_function)
            for k, v in obj.items()
        }
    elif isinstance(obj, (list, set, tuple)):
        t = type(obj)
        return t(deep_transform(o, transform_function) for o in obj)
    elif isinstance(obj, str):
        return transform_function(obj)
    else:
        return obj
