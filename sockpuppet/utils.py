try:
    from lxml import etree
    from io import StringIO
    from lxml.cssselect import CSSSelector
    HAS_LXML = True
except ImportError:
    HAS_LXML = False
    from bs4 import BeautifulSoup


def pascalcase(value: str) -> str:
    """capitalize the first letter of each _-separated component"""
    components = value.lower().split("_")
    # We capitalize the first letter of each component
    # with the 'capitalize' method and join them together.
    return "".join(x.capitalize() if x else "_" for x in components)


def camelcase(value: str) -> str:
    """capitalize the first letter of each _-separated component except the first one"""
    components = value.lower().split("_")
    return components[0] + "".join(x.capitalize() if x else "_" for x in components[1:])


def camelize_value(value):
    """camelizes all keys/values in a given dict or list"""
    if isinstance(value, list):
        value = [camelize_value(val) for val in value]
    elif isinstance(value, dict):
        value = {camelcase(key): camelize_value(val) for key, val in value.items()}
    return value


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
