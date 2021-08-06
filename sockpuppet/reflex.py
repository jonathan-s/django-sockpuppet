from django.urls import resolve
from urllib.parse import urlparse

from django.template.loader import render_to_string
from django.template.backends.django import Template
from django.test import RequestFactory

from .channel import Channel

PROTECTED_VARIABLES = [
    "broadcaster",
    "consumer",
    "context",
    "element",
    "identifier",
    "params",
    "permanent_attribute_name",
    "reflex_id",
    "selectors",
    "session",
    "url",
]


class Reflex:
    def __init__(
        self,
        consumer,
        url,
        element,
        selectors,
        params,
        identifier="",
        permanent_attribute_name=None,
        reflex_id=None,
    ):
        self.consumer = consumer
        self.context = {}
        self.element = element
        self.identifier = identifier
        self.is_morph = False
        self.params = params
        self.permanent_attribute_name = permanent_attribute_name
        self.reflex_id = reflex_id
        # TODO since this isn't used, we could remove this
        self.selectors = selectors
        self.session = consumer.scope["session"]
        self.url = url

        self._broadcaster = None
        self._init_run = True

    def __repr__(self):
        return f"<Reflex url: {self.url}, session: {self.get_channel_id()}>"

    def __setattr__(self, name, value):
        if name in PROTECTED_VARIABLES and getattr(self, "_init_run", None):
            raise ValueError("This instance variable is used by the reflex.")
        super().__setattr__(name, value)

    @property
    def broadcaster(self):
        if not self._broadcaster:
            self._broadcaster = Channel(
                self.get_channel_id(), identifier=self.identifier
            )
        return self._broadcaster

    def get_context_data(self, *args, **kwargs):
        if self.context:
            self.context.update(**kwargs)
            return self.context

        parsed_url = urlparse(self.url)
        resolved = resolve(parsed_url.path)
        view = resolved.func.view_class()
        view.request = self.request
        view.kwargs = resolved.kwargs

        # correct for detail and list views for django generic views
        if hasattr(view, "get_object"):
            view.object = view.get_object()

        if hasattr(view, "paginate_queryset"):
            view.object_list = view.get_queryset()

        context = view.get_context_data(**{"stimulus_reflex": True})

        self.context.update(context)
        self.context.update(**kwargs)
        return self.context

    def get_channel_id(self):
        """
        Override this to make the reflex send to a different channel
        other than the session_key of the user
        """
        return self.session.session_key

    @property
    def request(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        request.session = self.consumer.scope["session"]
        request.user = self.consumer.scope["user"]
        request.POST = self.params
        return request

    def reload(self):
        """A default reflex to force a refresh"""
        pass

    def morph(self, selector="", html="", template="", context={}):
        """
        If a morph is executed without any arguments, nothing is executed
        and the reflex won't send over any data to the frontend.
        """
        self.is_morph = True
        no_arguments = [not selector, not html, (not template and not context)]
        if all(no_arguments) and not selector:
            # an empty morph, nothing is sent ever.
            return

        if not selector:
            raise ValueError("No selector defined for morph")

        if html:
            html = html
        elif isinstance(template, Template):
            html = template.render(context)
        else:
            html = render_to_string(template, context)

        self.broadcaster.morph(
            {
                "selector": selector,
                "html": html,
                "children_only": True,
                "permanent_attribute_name": self.permanent_attribute_name,
                "stimulus_reflex": {
                    "morph": "selector",
                    "reflexId": self.reflex_id,
                    "url": self.url,
                },
            }
        )
        self.broadcaster.broadcast()
