from django import template
from django.template import Template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


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
                msg = '{} is not yet handled'.format(node.token.token_type.name)
                raise Exception(msg)
            output = output + raw
        return output


@register.simple_tag
def reflex(controller, **kwargs):
    """
    Adds the necessary data-reflex tag to handle a click element on the respective element
    :param controller: Name of the Reflex Controller and Method ({controller}#{handler}).
    :param kwargs: Further data- attributes that should be passed to the handler
    """
    # TODO Validate that the reflex is present and can be handled
    data = ' '.join([f'data-{key}="{escape(val)}"' for key, val in kwargs.items()])
    return mark_safe(f'data-reflex="click->{controller}" {data}')
