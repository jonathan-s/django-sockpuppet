from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from inflector import Inflector

inflector = Inflector()


def camelize(word):
    word = inflector.camelize(word)
    return '{}{}'.format(word[0].lower(), word[1:])


class Channel:

    def __init__(self, name):
        self.name = name
        self.operations = self.stub()

    def clear(self):
        self.operations = self.stub()

    def add_operation(self, key, options):
        self.operations[key].append(options)

    def stub(self):
        return {
            'dispatch_event': [],
            'morph': [],
            'inner_html': [],
            'outer_html': [],
            'text_content': [],
            'insert_adjacent_html': [],
            'insert_adjacent_text': [],
            'remove': [],
            'set_value': [],
            'set_attribute': [],
            'remove_attribute': [],
            'add_css_class': [],
            'remove_css_class': [],
            'set_dataset_property': [],
        }

    def broadcast(self):
        '''
        Figure out the structure of this..
        '''
        operations = {
            camelize(key): value
            for key, value in self.operations.items() if value
        }
        channel_layer = get_channel_layer()
        group_send = async_to_sync(channel_layer.group_send)
        group_send(
            self.name,
            {
                "type": "message",
                "cableReady": True,
                "operations": operations
            }
        )
        self.clear()

    def dispatch(self, options={}):
        '''
        dispatch_event: [{
                name:     "string",
                detail:   "object",
                selector: "string",
            }, ...
        ],
        '''
        self.add_operation('dispatch_event', options)

    def morph(self, options={}):
        '''
        morph: [{
                selector:      "string",
                html:          "string"
                children_only:  true|false,
                permanent_attribute_name: "string",
                focus_selector: "string",
            }, ...
        ],
        '''
        self.add_operation('morph', options)

    def inner_html(self, options={}):
        '''
           inner_html: [{
             selector:      "string",
             focus_selector: "string",
             html:          "string"
           }, ...],
        '''
        self.add_operation('inner_html', options)

    def outer_html(self, options={}):
        '''
           outer_html: [{
             selector:      "string",
             focus_selector: "string",
             html:          "string"
           }, ...],
        '''
        self.add_operation('outer_html', options)

    def text_content(self, options={}):
        '''
           text_content: [{
             selector: "string",
             text:     "string"
           }, ...]
        '''
        self.add_operation('text_content', options)

    def insert_adjacent_html(self, options={}):
        '''
        insert_adjacent_html: [{
            selector:      "string",
            focus_selector: "string",
            position:      "string",
            html:          "string"
        }, ...],
        '''
        self.add_operation('insert_adjacent_html', options)

    def remove(self, options={}):
        '''
        remove: [{
            selector:      "string",
            focus_selector: "string,
        }, ...],
        '''
        self.add_operation('remove', options)

    def set_value(self, options={}):
        '''
        set_value: [{
            selector: "string",
            value:    "string"
        }, ...],
        '''
        self.add_operation('set_value', options)

    def set_attribute(self, options={}):
        '''
        set_attribute: [{
            selector: "string",
            name:     "string",
            value:    "string"
        }, ...],
        '''
        self.add_operation('set_attribute', options)

    def remove_attribute(self, options={}):
        '''
        remove_attribute: [{
            selector: "string",
            name:     "string"
        }, ...],
        '''
        self.add_operation('remove_attribute', options)

    def add_css_class(self, options={}):
        '''
        add_css_class: [{
            selector: "string",
            name:     "string"
        }, ...],
        '''
        self.add_operation('add_css_class', options)

    def remove_css_class(self, options={}):
        '''
        remove_css_class: [{
            selector: "string",
            name:     "string"
        }, ...],
        '''
        self.add_operation('remove_css_class', options)

    def set_dataset_property(self, options):
        '''
        set_dataset_property: [{
            selector: "string",
            name:     "string",
            value:    "string"
        }, ...],
        '''
        self.add_operation('set_dataset_property', options)
