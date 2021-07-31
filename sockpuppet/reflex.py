from collections import UserDict
from django.urls import resolve
from urllib.parse import urlparse

from django.test import RequestFactory

PROTECTED_VARIABLES = [
    "consumer",
    "context",
    "element",
    "params",
    "selectors",
    "session",
    "url",
]


class Context(UserDict):
    """
    This class represents the context that will be rendered in a template
    and then sent client-side through websockets.

    It works just like a dictionary with the extension that you can set and get
    data through dot access.

    > context.my_data = 'hello'
    > context.my_data  # 'hello'
    """
    # NOTE for maintainer
    # A dictionary that keeps track of whether it's been used as dictionary
    # or if values has been set with dot notation. We expect things to be set
    # in dot notation so a warning is issued until next major version (1.0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attr_data = {}

    def __getitem__(self, key):
        data = self.__dict__
        if (
            data["data"].get(key, KeyError) is KeyError
            and data["_attr_data"].get(key, KeyError) is KeyError
        ):
            raise KeyError(key)
        return self.data.get(key) or self._attr_data.get(key)

    def __setitem__(self, key, item):
        if not self.__dict__.get("data"):
            self.__dict__["data"] = {}
        self.__dict__["data"][key] = item

    def __getattr__(self, key):
        if not self.__dict__.get("data"):
            self.__dict__["data"] = {}
        if not self.__dict__.get("_attr_data"):
            self.__dict__["_attr_data"] = {}

        if (
            self.__dict__["data"].get(key, KeyError) is KeyError
            and self.__dict__["_attr_data"].get(key, KeyError) is KeyError
        ):
            raise AttributeError(key)
        result = self.data.get(key) or self._attr_data.get(key)
        return result

    def __setattr__(self, key, value):
        if not self.__dict__.get("_attr_data"):
            self.__dict__["_attr_data"] = {}
        self.__dict__["_attr_data"][key] = value


class Reflex:
    def __init__(self, consumer, url, element, selectors, params):
        self.consumer = consumer
        self.context = Context()
        self.element = element
        self.params = params
        self.selectors = selectors
        self.session = consumer.scope["session"]
        self.url = url

        self._init_run = True

    def __repr__(self):
        return f"<Reflex url: {self.url}, session: {self.get_channel_id()}>"

    def __setattr__(self, name, value):
        if name in PROTECTED_VARIABLES and getattr(self, "_init_run", None):
            raise ValueError("This instance variable is used by the reflex.")
        super().__setattr__(name, value)

    def get_context_data(self, *args, **kwargs):
        """
        Fetches the context from the view which the reflex belongs to.
        Once you've made modifications you can update the reflex context.

        > context = self.get_context_data()
        > context['a_key'] = 'some data'
        > self.context.update(context)
        """

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
        """A synthetic request used to mimic the request-response cycle"""
        factory = RequestFactory()
        request = factory.get(self.url)
        request.session = self.consumer.scope["session"]
        request.user = self.consumer.scope["user"]
        request.POST = self.params
        return request

    def reload(self):
        """
        A default reflex to force a refresh, when used in html it will
        refresh the page

        data-action="click->MyReflexClass#reload"
        """
        pass
