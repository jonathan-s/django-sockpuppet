import re
try:
    from lxml import etree
    from io import StringIO
    from lxml.cssselect import CSSSelector
    HAS_LXML = True
except ImportError:
    HAS_LXML = False
    from bs4 import BeautifulSoup


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


def _lxml_selectors(html, selectors):
    parser = etree.HTMLParser()

    document = etree.parse(StringIO(html), parser)
    selectors = [CSSSelector(selector) for selector in selectors]
    selectors = [selector for selector in selectors if selector(document)]
    return document, selectors


def _bs_selectors(html, selectors):
    document = BeautifulSoup(html)
    selectors = [selector for selector in selectors if document.select(selector)]
    return document, selectors


def get_document_and_selectors(html, selectors):
    if HAS_LXML:
        return _lxml_selectors(html, selectors)
    return _bs_selectors(html, selectors)


def parse_out_html(document, selector):
    if HAS_LXML:
        return ''.join(
            [etree.tostring(e, method="html").decode('utf-8') for e in selector(document)]
        )
    return ''.join([e.decode_contents() for e in document.select(selector)])
