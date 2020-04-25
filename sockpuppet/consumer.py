import json
import logging
from importlib import import_module
from functools import wraps
import inspect
from os import walk
from urllib.parse import urlparse

from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from channels.generic.websocket import JsonWebsocketConsumer
from django.apps import apps
from django.urls import resolve

from .channel import Channel
from .reflex import PROTECTED_VARIABLES
from .element import Element
from .utils import classify


logger = logging.getLogger('sockpuppet')


class SockpuppetError(Exception):
    pass


def context_decorator(method, extra_context):
    @wraps(method)
    def wrapped(self, *method_args, **method_kwargs):
        context = method(self, *method_args, **method_kwargs)
        context.update(extra_context)
        return context
    return wrapped


class SockpuppetConsumer(JsonWebsocketConsumer):
    reflexes = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriptions = set()

        if not self.reflexes:
            configs = apps.app_configs.values()
            for config in configs:
                self.load_reflexes_from_config(config)

    def connect(self):
        super().connect()
        session = self.scope['session']
        if not session.session_key:
            # normally there is no session key for anonymous users.
            session.save()

        async_to_sync(self.channel_layer.group_add)(
            session.session_key,
            self.channel_name
        )
        logger.debug(
            ':: CONNECT: Channel %s session: %s',
            self.channel_name, session.session_key
        )

    def disconnect(self, *args, **kwargs):
        session = self.scope['session']
        async_to_sync(self.channel_layer.group_discard)(
            session.session_key,
            self.channel_name
        )
        logger.debug(
            ':: DISCONNECT: Channel %s session: %s',
            self.channel_name, session.session_key
        )
        super().disconnect(*args, **kwargs)

    def load_reflexes_from_config(self, config):
        def append_reflex(module):
            for classname in dir(module):
                if 'reflex' in classname.lower():
                    ReflexClass = getattr(module, classname)
                    self.reflexes[ReflexClass.__name__] = ReflexClass

        path = config.module.__path__[0]
        for dirpath, dirnames, filenames in walk(path):
            if dirpath == path and 'reflexes' in dirnames:
                # classes in reflexes.py
                import_path = '{}.reflexes'.format(config.name)
                module = import_module(import_path)
                append_reflex(module)
            elif dirpath == '{}/{}'.format(path, 'reflexes'):
                # assumes reflexes folder is placed directly in app.
                import_path = '{config_name}.reflexes.{reflex_file}'
                for filename in filenames:
                    name = filename.split('.')[0]
                    full_import_path = import_path.format(
                        config_name=config.name, reflex_file=name
                    )
                    module = import_module(full_import_path)
                    append_reflex(module)

    def message(self, event):
        logger.debug(event)
        self.send(json.dumps(event))

    def receive_json(self, data, **kwargs):
        logger.debug('Json: %s', data)
        logger.debug('kwargs: %s', kwargs)

        url = data['url']
        selectors = data['selectors'] if data['selectors'] else ['body']
        target = data['target']
        reflex_name, method_name = target.split('#')
        reflex_name = classify(reflex_name)
        arguments = data['args'] if data.get('args') else []
        element = Element(data['attrs'])
        try:
            ReflexClass = self.reflexes.get(reflex_name)
            if not self.is_reflex(ReflexClass):
                msg = '{} is not of the class SockpuppetReflex'
                raise ValueError(msg)
            reflex = ReflexClass(self, url=url, element=element, selectors=selectors)
            self.delegate_call_to_reflex(reflex, method_name, arguments)
        except ValueError as e:
            msg = 'SockpuppetConsumer failed to invoke {target}, {url}, {message}'.format(
                target=target, url=url, message=e.message
            )
            return self.broadcast_error(msg, data)
            raise SockpuppetError(msg)

        try:
            self.render_page_and_broadcast_morph(reflex, selectors, data)
        except Exception as e:
            message = 'SockpuppetConsumer failed to re-render {url} {message}'.format(
                url=url, message=e.message
            )
            self.broadcast_error(message, data)
            raise SockpuppetError(message)

    def render_page_and_broadcast_morph(self, reflex, selectors, data):
        html = self.render_page(reflex)
        if html:
            self.broadcast_morphs(selectors, data, html)

    def render_page(self, reflex):
        parsed_url = urlparse(reflex.url)
        url_path = parsed_url.path + parsed_url.query
        resolved = resolve(url_path)
        view = resolved.func

        instance_variables = [
            name for (name, member) in inspect.getmembers(reflex)
            if not name.startswith('__') and name not in PROTECTED_VARIABLES
        ]
        reflex_context = {key: getattr(reflex, key) for key in instance_variables}
        reflex_context['stimulus_reflex'] = True

        original_context_data = view.view_class.get_context_data
        view.view_class.get_context_data = context_decorator(
            view.view_class.get_context_data, reflex_context
        )
        response = view(reflex.request, resolved.args, resolved.kwargs)
        # we've got the response, the function needs to work as normal again
        view.view_class.get_context_data = original_context_data
        reflex.session.save()
        return response.rendered_content

    def broadcast_morphs(self, selectors, data, html):
        document = BeautifulSoup(html)
        selectors = [selector for selector in selectors if document.select(selector)]

        channel = Channel(self.scope['session'].session_key)
        logger.debug('Broadcasting to %s', self.scope['session'].session_key)
        for selector in selectors:
            channel.morph({
                'selector': selector,
                'html': [str(e) for e in document.select(selector)],
                'children_only': True,
                'permanent_attribute_name': data['permanent_attribute_name'],
                'stimulus_reflex': {'url': data['url']}
            })
        channel.broadcast()

    def is_reflex(self, reflex_class):
        # TODO fix this
        return True

    def delegate_call_to_reflex(self, reflex, method_name, arguments):
        method = getattr(reflex, method_name)
        method_signature = inspect.signature(method)
        if len(method_signature.parameters) == 0:
            getattr(reflex, method_name)()
        else:
            getattr(reflex, method_name)(*arguments)

    def broadcast_error(self, message, data):
        raise NotImplementedError()
