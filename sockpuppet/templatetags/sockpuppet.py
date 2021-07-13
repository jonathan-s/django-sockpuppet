from django import template
from django.template import Template
from sockpuppet.utils import camelcase, pascalcase

register = template.Library()

register.filter(name="camelcase", filter_func=camelcase)
register.filter(name="pascalcase", filter_func=pascalcase)


@register.tag(name="raw")
def raw(parser, token):
    nodelist = parser.parse(('endraw',))
    parser.delete_first_token()
    return RawNode(nodelist)


class RawNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = ''
        for node in self.nodelist:
            if node.token.token_type.name == 'BLOCK':
                template = Template(node.token.contents)
                rendered = template.render(context)
                raw = '{% ' + rendered + ' %}'
            elif node.token.token_type.name == 'VAR':
                raw = '{{ ' + node.token.contents + ' }}'
            else:
                raw = node.token.contents
            output = output + raw
        return output
