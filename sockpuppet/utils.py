from inflector import Inflector

inflector = Inflector()


def camelize(word):
    word = inflector.camelize(word)
    return '{}{}'.format(word[0].lower(), word[1:])
