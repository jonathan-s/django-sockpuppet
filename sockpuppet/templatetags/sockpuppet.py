from django import template
from django.template import Template, RequestContext
from django.template.base import Token, VariableNode, FilterExpression
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
    return generate_reflex_attributes('click', controller, kwargs)


def generate_reflex_attributes(action, controller, parameters):
    data = ' '.join([f'data-{key}="{val}"' for key, val in parameters.items()])
    return mark_safe(f'data-reflex="{action}->{controller}" {data}')


@register.tag
def stimulus_controller(parser, token, **kwargs):
    _, controller = token.split_contents()
    nodelist = parser.parse(('endcontroller',))
    parser.delete_first_token()
    controller = controller.strip("'").strip('"')
    return StimulusNode(controller, nodelist)


class ReflexNode(template.Node):

    def __init__(self, action, reflex, controller=None, parameters={}):
        self.action = action
        self.reflex = reflex
        self.controller = controller
        self.parameters = parameters

    def render(self, context: RequestContext):
        # First, check if the "reflex" given is a VariableNode. We check to extract stuff from it
        parameters = {}
        if isinstance(self.reflex, VariableNode):
            var_name = self.reflex.filter_expression.token
            param = context.get(var_name)

            if param is None:
                raise Exception(f"The given Variable '{var_name}' was not found in the context!")

            if 'controller' not in param or 'reflex' not in param:
                raise Exception(f"The given object with name '{var_name}' needs to have attributes 'controller' and 'reflex'")
            else:
                self.controller = param['controller']
                self.reflex = param['reflex']
                parameters.update({k: param[k] for k in param.keys() if k not in ('controller', 'reflex')})
        if self.controller is None:
            raise Exception(
                "A ClickReflex tag can only be used inside a stimulus controller or needs an explicit controller set!")

        for k, v in self.parameters.items():
            if isinstance(v, VariableNode):
                value = v.render(context)
            else:
                value = v
            parameters.update({k: value})
        return generate_reflex_attributes(self.action, f'{self.controller}#{self.reflex}', parameters)


def extract_string_or_node(text):
    stripped = text.strip("'").strip('"')
    is_numeric = False
    try:
        int(stripped)
        is_numeric = True
    except:
        pass
    if text == stripped and not is_numeric:
        return VariableNode(FilterExpression(text, parser=None))
    else:
        return stripped


@register.tag("click_reflex")
def click_reflex(parser, token: Token):
    controller, kwargs, reflex = parse_reflex_token(token)
    return ReflexNode('click', reflex, controller=controller, parameters=kwargs)


@register.tag("submit_reflex")
def submit_reflex(parser, token: Token):
    controller, kwargs, reflex = parse_reflex_token(token)
    return ReflexNode('submit', reflex, controller=controller, parameters=kwargs)


@register.tag("input_reflex")
def submit_reflex(parser, token: Token):
    controller, kwargs, reflex = parse_reflex_token(token)
    return ReflexNode('input', reflex, controller=controller, parameters=kwargs)


def parse_reflex_token(token):
    splitted = token.split_contents()[1:]
    args = []
    kwargs = {}
    for s in splitted:
        if s.__contains__("="):
            k, v = s.split("=")
            kwargs.update({k: extract_string_or_node(v)})
        else:
            args.append(extract_string_or_node(s))
    if len(args) == 1:
        reflex = args[0]
        controller = None
    elif len(args) == 2:
        controller = args[0]
        reflex = args[1]
    else:
        raise Exception('Only one or two non-kv parameters can be given!')
    return controller, kwargs, reflex


class StimulusNode(template.Node):

    def __init__(self, controller, nodelist):
        self.controller = controller
        self.nodelist = nodelist

    def render(self, context):
        for node in self.nodelist:
            if isinstance(node, ReflexNode):
                node.controller = self.controller
        output = self.nodelist.render(context)
        return output
