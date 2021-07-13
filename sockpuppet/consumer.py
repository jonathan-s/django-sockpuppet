import time
import json
import logging
from importlib import import_module
import inspect
from functools import wraps
from os import walk, path
from urllib.parse import urlparse
from urllib.parse import parse_qsl

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.apps import apps
from django.urls import resolve
from django.conf import settings

from .channel import Channel
from .reflex import PROTECTED_VARIABLES, Reflex
from .element import Element
from .utils import get_document_and_selectors, parse_out_html


logger = logging.getLogger("sockpuppet")


class SockpuppetError(Exception):
    pass


def context_decorator(method, extra_context):
    @wraps(method)
    def wrapped(self, *method_args, **method_kwargs):
        method_kwargs.update(extra_context)
        context = method(self, *method_args, **method_kwargs)
        # if context was picked from cache extra context needs to be added again
        context.update(extra_context)
        return context

    return wrapped


class BaseConsumer(JsonWebsocketConsumer):
    reflexes = {}
    subscriptions = set()

    def _get_channelname(self, channel_name):
        try:
            # StimulusReflex sends the channel name in the format
            # of a json blob for name.
            name = json.loads(channel_name)
            name = name["channel"].replace("::", "-")
        except json.decoder.JSONDecodeError:
            name = channel_name
        return name

    def connect(self):
        """
        We use the user session key as a default channel to publish any events
        """
        super().connect()
        session = self.scope["session"]
        has_session_key = session.session_key

        if not has_session_key:
            # normally there is no session key for anonymous users.
            session.save()

        async_to_sync(self.channel_layer.group_add)(
            session.session_key, self.channel_name
        )

        if not has_session_key:
            self.group_send(
                self.scope["session"].session_key,
                {
                    "type": "message",
                    "meta_type": "cookie",
                    "key": "sessionid",
                    "value": session.session_key,
                    "max_age": settings.SESSION_COOKIE_AGE,
                },
            )

        logger.debug(
            ":: CONNECT: Channel %s session: %s", self.channel_name, session.session_key
        )

    def disconnect(self, *args, **kwargs):
        """
        When we disconnect we unsubscribe from the user session key.
        """
        session = self.scope["session"]
        async_to_sync(self.channel_layer.group_discard)(
            session.session_key, self.channel_name
        )
        logger.debug(
            ":: DISCONNECT: Channel %s session: %s",
            self.channel_name,
            session.session_key,
        )
        super().disconnect(*args, **kwargs)

    def subscribe(self, data, **kwargs):
        name = self._get_channelname(data["channelName"])
        logger.debug("Subscribe %s to %s", self.channel_name, name)
        async_to_sync(self.channel_layer.group_add)(name, self.channel_name)

    def unsubscribe(self, data, **kwargs):
        name = self._get_channelname(data["channelName"])
        async_to_sync(self.channel_layer.group_discard)(name, self.channel_name)

    def receive_json(self, data, **kwargs):
        message_type = data.get("type")
        if message_type is None and data.get("target"):
            self.reflex_message(data, **kwargs)
        elif message_type == "subscribe":
            self.subscribe(data, **kwargs)
        elif message_type == "unsubscribe":
            self.unsubscribe(data, **kwargs)
        else:
            print("Unsupported")

    def message(self, event):
        logger.debug("Sending data: %s", event)
        self.send(json.dumps(event))

    def group_send(self, recipient, message):
        send = async_to_sync(self.channel_layer.group_send)
        send(recipient, message)

    def load_reflexes(self):
        configs = apps.app_configs.values()
        for config in configs:
            self.load_reflexes_from_config(config)

    def load_reflexes_from_config(self, config):
        def append_reflex():
            self.reflexes.update(
                {
                    ReflexClass.__name__: ReflexClass
                    for ReflexClass in Reflex.__subclasses__()
                }
            )

        modpath = config.module.__path__[0]

        for dirpath, dirnames, filenames in walk(modpath):
            if dirpath == modpath and "reflexes.py" in filenames:
                # classes in reflexes.py
                import_path = "{}.reflexes".format(config.name)
                import_module(import_path)
                append_reflex()

            elif dirpath == path.join(modpath, "reflexes"):
                # assumes reflexes folder is placed directly in app.
                import_path = "{config_name}.reflexes.{reflex_file}"

                for filename in filenames:
                    # eliminates empty values in the filename before getting the
                    # module name from the filename.
                    name = [file for file in filename.split(".") if file][0]
                    full_import_path = import_path.format(
                        config_name=config.name, reflex_file=name
                    )
                    import_module(full_import_path)
                    append_reflex()

    def reflex_message(self, data, **kwargs):
        logger.debug("Json: %s", data)
        logger.debug("kwargs: %s", kwargs)
        start = time.perf_counter()

        url = data["url"]
        selectors = data["selectors"] if data["selectors"] else ["body"]
        target = data["target"]
        reflex_class_name, method_name = target.split("#")
        arguments = data["args"] if data.get("args") else []
        params = dict(parse_qsl(data["formData"]))
        element = Element(data["attrs"])
        if not self.reflexes:
            self.load_reflexes()

        try:
            ReflexClass = self.reflexes.get(reflex_class_name)
            reflex = ReflexClass(
                self, url=url, element=element, selectors=selectors, params=params
            )
            self.delegate_call_to_reflex(reflex, method_name, arguments)
        except TypeError as exc:
            if not self.reflexes.get(reflex_class_name):
                msg = f"Sockpuppet tried to find a reflex class called {reflex_class_name}. Are you sure such a class exists?"  # noqa
                self.broadcast_error(msg, data)
            else:
                msg = str(exc)
                self.broadcast_error(msg, data)
            logging.exception(msg)
            return
        except Exception as e:
            error = "{}: {}".format(e.__class__.__name__, str(e))
            msg = "SockpuppetConsumer failed to invoke {target}, with url {url}. {message}".format(
                target=target, url=url, message=error
            )
            self.broadcast_error(msg, data, None)
            logging.exception(msg)
            return

        try:
            self.render_page_and_broadcast_morph(reflex, selectors, data)
        except Exception as e:
            error = "{}: {}".format(e.__class__.__name__, str(e))
            msg = "SockpuppetConsumer failed to re-render {url} {message}".format(
                url=url, message=error
            )
            self.broadcast_error(msg, data, reflex)
            logging.exception(msg)
            return

        logger.debug("Reflex took %6.2fms", (time.perf_counter() - start) * 1000)

    def render_page_and_broadcast_morph(self, reflex, selectors, data):
        html = self.render_page(reflex)
        if html:
            self.broadcast_morphs(selectors, data, html, reflex)

    def render_page(self, reflex):
        parsed_url = urlparse(reflex.url)
        resolved = resolve(parsed_url.path)
        view = resolved.func

        instance_variables = [
            name
            for (name, member) in inspect.getmembers(reflex)
            if not name.startswith("__") and name not in PROTECTED_VARIABLES
        ]
        reflex_context = {key: getattr(reflex, key) for key in instance_variables}
        reflex_context["stimulus_reflex"] = True

        original_context_data = view.view_class.get_context_data
        reflex.get_context_data(**reflex_context)
        # monkey patch context method
        view.view_class.get_context_data = reflex.get_context_data
        # We also need to make sure that the last update from reflex context wins
        view.view_class.get_context_data = context_decorator(
            view.view_class.get_context_data, reflex_context
        )

        response = view(reflex.request, *resolved.args, **resolved.kwargs)
        # we've got the response, the function needs to work as normal again
        view.view_class.get_context_data = original_context_data
        reflex.session.save()
        return response.rendered_content

    def broadcast_morphs(self, selectors, data, html, reflex):
        document, selectors = get_document_and_selectors(html, selectors)

        channel = Channel(reflex.get_channel_id(), identifier=data["identifier"])
        logger.debug("Broadcasting to %s", reflex.get_channel_id())

        # TODO can be removed once stimulus-reflex has increased a couple of versions
        permanent_attribute_name = data.get("permanent_attribute_name")
        if not permanent_attribute_name:
            # Used in stimulus-reflex >= 3.4
            permanent_attribute_name = data["permanentAttributeName"]

        for selector in selectors:
            # cssselect has an attribute css
            plain_selector = getattr(selector, "css", selector)
            channel.morph(
                {
                    "selector": plain_selector,
                    "html": parse_out_html(document, selector),
                    "children_only": True,
                    "permanent_attribute_name": permanent_attribute_name,
                    "stimulus_reflex": {**data},
                }
            )
        channel.broadcast()

    def delegate_call_to_reflex(self, reflex, method_name, arguments):
        method = getattr(reflex, method_name)
        method_signature = inspect.signature(method)
        if len(method_signature.parameters) == 0:
            getattr(reflex, method_name)()
        else:
            getattr(reflex, method_name)(*arguments)

    def broadcast_error(self, message, data, reflex=None):
        # We may have a sitation where we weren't able to get a reflex
        session_key = (
            reflex.get_channel_id() if reflex else self.scope["session"].session_key
        )
        channel = Channel(session_key, identifier=data["identifier"])
        data.update(
            {
                "serverMessage": {
                    "subject": "error",
                    "body": message,
                }
            }
        )
        channel.dispatch_event(
            {
                "name": "stimulus-reflex:server-message",
                "detail": {"stimulus_reflex": data},
            }
        )
        channel.broadcast()


class SockpuppetConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.reflexes:
            self.load_reflexes()


class SockpuppetConsumerAsgi(BaseConsumer):
    """
    This consumer supports the asgi standard now in django
    This consumer should be used when using channels 3.0.0 and upwards
    """

    async def __call__(self, scope, receive, send):
        await super().__call__(scope, receive, send)

        if not self.reflexes:
            self.load_reflexes()
