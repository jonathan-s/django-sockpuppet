from inflector import Inflector

inflector = Inflector()


def camelize(word):
    word = inflector.camelize(word)
    return '{}{}'.format(word[0].lower(), word[1:])


def classify(word):
    tail = camelize(word[1:])
    head = word[:1].title()
    return '{}{}'.format(head, tail)
