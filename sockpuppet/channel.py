import json
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .utils import camelize_value, camelcase

logger = logging.getLogger(__name__)


class Channel:
    """
    Accepts a name which should either be the name of the group
    or the channel_name to which the content will be broadcast to.

    Frontend makes a lookup against the identifier, if the identifier
    exists it executes the reflex operations. If the identifier does not
    exist, nothing will happen.

    If you're using this and initializes this with the session key as a name.
    You need to set the identifier to '{"channel":"StimulusReflex::Channel"}'
    which is the default identifier in the frontend.
    """

    def __init__(self, name, identifier=""):
        if not identifier:
            identifier = json.dumps({"channel": name}).replace(" ", "")
        self.identifier = identifier
        self.name = name
        self.operations = self.stub()

    def clear(self):
        self.operations = self.stub()

    def add_operation(self, key, options):
        self.operations[key].append(options)

    def stub(self):
        return {
            "add_css_class": [],
            "dispatch_event": [],
            "inner_html": [],
            "insert_adjacent_html": [],
            "insert_adjacent_text": [],
            "morph": [],
            "outer_html": [],
            "remove_attribute": [],
            "remove_css_class": [],
            "remove": [],
            "set_attribute": [],
            "set_dataset_property": [],
            "set_style": [],
            "set_value": [],
            "text_content": [],
        }

    def broadcast(self):
        operations = {
            camelcase(key): camelize_value(value)
            for key, value in self.operations.items()
            if value
        }
        channel_layer = get_channel_layer()
        group_send = async_to_sync(channel_layer.group_send)
        group_send(
            self.name,
            {
                "identifier": self.identifier,
                "type": "message",
                "cableReady": True,
                "operations": operations,
            },
        )
        self.clear()

    def dispatch_event(self, options={}, **kwargs):
        """
        name:       "string",   # required - the name of the DOM event to dispatch (can be custom)
        detail:     {},         # [null]   - assigned to event.detail
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # [document] - string containing a CSS selector or XPath expression
        xpath:      true|false  # [false] - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("dispatch_event", options)
        return self

    def morph(self, options={}, **kwargs):
        """
        cancel:                   true|false, # [false]  - cancel the operation (for use on client)
        children_only:            true|false, # [false]  - indicates if only child nodes should be morphed... skipping the parent element
        focus_selector:           "string",   # [null]   - string containing a CSS selector
        html:                     "string",   # [null]   - the HTML to assign
        permanent_attribute_name: "string",   # [null]   - an attribute name that prevents elements from being updated i.e. "data-permanent"
        select_all:               true|false, # [false]  - operate on list of elements returned from selector
        selector:                 "string",   # required - string containing a CSS selector or XPath expression
        xpath:                    true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("morph", options)
        return self

    def inner_html(self, options={}, **kwargs):
        """
        cancel:         true|false, # [false]  - cancel the operation (for use on client)
        focus_selector: "string",   # [null]   - string containing a CSS selector
        html:           "string",   # [null]   - the HTML to assign
        select_all:     true|false, # [false]  - operate on list of elements returned from selector
        selector:       "string",   # required - string containing a CSS selector or XPath expression
        xpath:          true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("inner_html", options)
        return self

    def outer_html(self, options={}, **kwargs):
        """
        cancel:         true|false, # [false]  - cancel the operation (for use on client)
        focus_selector: "string",   # [null]   - string containing a CSS selector
        html:           "string",   # [null]   - the HTML to use as replacement
        select_all:     true|false, # [false]  - operate on list of elements returned from selector
        selector:       "string",   # required - string containing a CSS selector or XPath expression
        xpath:          true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("outer_html", options)
        return self

    def text_content(self, options={}, **kwargs):
        """
        cancel:         true|false,     # [false]  - cancel the operation (for use on client)
        focus_selector: "string",       # [null]   - string containing a CSS selector
        select_all:     true|false,     # [false]  - operate on list of elements returned from selector
        selector:       "string",       # required - string containing a CSS selector or XPath expression
        text:           "string",       # [null]   - the text to assign
        xpath:          true|false      # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("text_content", options)
        return self

    def insert_adjacent_html(self, options={}, **kwargs):
        """
        cancel:         true|false, # [false]     - cancel the operation (for use on client)
        focus_selector: "string",   # [null]      - string containing a CSS selector
        html:           "string",   # [null]      - the HTML to insert
        position:       "string",   # [beforeend] - the relative position to the DOM element (beforebegin, afterbegin, beforeend, afterend)
        select_all:     true|false, # [false]     - operate on list of elements returned from selector
        selector:       "string",   # required    - string containing a CSS selector or XPath expression
        xpath:          true|false  # [false]     - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("insert_adjacent_html", options)
        return self

    def remove(self, options={}, **kwargs):
        """
        cancel:         true|false, # [false]  - cancel the operation (for use on client)
        focus_selector: "string",   # [null]   - string containing a CSS selector
        select_all:     true|false, # [false]  - operate on list of elements returned from selector
        selector:       "string",   # required - string containing a CSS selector or XPath expression
        xpath:          true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("remove", options)
        return self

    def remove_attribute(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        name:       "string",   # required - the attribute to remove
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("remove_attribute", options)
        return self

    def set_attribute(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        name:       "string",   # required - the attribute to set
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        value:      "string",   # [null]   - the value to assign to the attribute
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("set_attribute", options)
        return self

    def set_value(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        value:      "string",   # [null]   - the value to assign to the attribute
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("set_value", options)
        return self

    def add_css_class(self, options={}, **kwargs):
        """
        cancel:     true|false,      # [false]  - cancel the operation (for use on client)
        name:       "string/array",  # [null]   - string or array containing the CSS class name to add
        select_all: true|false,      # [false]  - operate on list of elements returned from selector
        selector:   "string",        # required - string containing a CSS selector or XPath expression
        xpath:      true|false       # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("add_css_class", options)
        return self

    def remove_css_class(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        name:       "string",   # [null]   - string containing the CSS class name to remove
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("remove_css_class", options)
        return self

    def set_dataset_property(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        name:       "string",   # required - the property to set, camelCased
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        value:      "string",   # [null]   - the value to assign to the dataset
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("set_dataset_property", options)
        return self

    def set_style(self, options={}, **kwargs):
        """
        cancel:     true|false, # [false]  - cancel the operation (for use on client)
        select_all: true|false, # [false]  - operate on list of elements returned from selector
        selector:   "string",   # required - string containing a CSS selector or XPath expression
        styles: {
            background: "red",
            color: "white"
        },
        xpath:      true|false  # [false]  - process the selector as an XPath expression
        """
        options.update(kwargs)
        self.add_operation("set_style", options)
        return self
