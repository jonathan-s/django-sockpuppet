import time
import json
import logging
from importlib import import_module
from functools import wraps
import inspect
from os import walk, path
from urllib.parse import urlparse

from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from channels.generic.websocket import JsonWebsocketConsumer
from django.apps import apps
from django.urls import resolve
from django.conf import settings

from .channel import Channel
from .reflex import PROTECTED_VARIABLES
from .element import Element
from .utils import classify, camelize_value


logger = logging.getLogger('sockpuppet')


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
        has_session_key = session.session_key

        if not has_session_key:
            # normally there is no session key for anonymous users.
            session.save()

        async_to_sync(self.channel_layer.group_add)(
            session.session_key,
            self.channel_name
        )

        if not has_session_key:
            self.group_send(
                self.scope['session'].session_key,
                {
                    'type': 'message',
                    'meta_type': 'cookie',
                    'key': 'sessionid',
                    'value': session.session_key,
                    'max_age': settings.SESSION_COOKIE_AGE
                }
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

    def group_send(self, recipient, message):
        send = async_to_sync(self.channel_layer.group_send)
        send(recipient, message)

    def load_reflexes_from_config(self, config):
        def append_reflex(module):
            # TODO only import classes that are actually that inherits Reflex
            for classname in dir(module):
                if 'reflex' in classname.lower():
                    ReflexClass = getattr(module, classname)
                    self.reflexes[ReflexClass.__name__] = ReflexClass

        modpath = config.module.__path__[0]

        for dirpath, dirnames, filenames in walk(modpath):
            if dirpath == modpath and 'reflexes.py' in filenames:
                # classes in reflexes.py
                import_path = '{}.reflexes'.format(config.name)
                module = import_module(import_path)

                append_reflex(module)
            elif dirpath == path.join(modpath, 'reflexes'):
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
        session_key = self.scope['session'].session_key
        logger.debug('Sending data to session: %s, %s', session_key, event)
        self.send(json.dumps(event))

    def receive_json(self, data, **kwargs):
        logger.debug('Json: %s', data)
        logger.debug('kwargs: %s', kwargs)
        start = time.time()

        url = data['url']
        selectors = data['selectors'] if data['selectors'] else ['body']
        target = data['target']
        reflex_name, method_name = target.split('#')
        reflex_name = classify(reflex_name)
        arguments = data['args'] if data.get('args') else []
        element = Element(data['attrs'])
        try:
            ReflexClass = self.reflexes.get(reflex_name)
            reflex = ReflexClass(self, url=url, element=element, selectors=selectors)
            self.delegate_call_to_reflex(reflex, method_name, arguments)
        except Exception as e:
            error = '{}: {}'.format(e.__class__.__name__, str(e))
            msg = 'SockpuppetConsumer failed to invoke {target}, with url {url}, {message}'.format(
                target=target, url=url, message=error
            )
            self.broadcast_error(msg, data)
            raise SockpuppetError(msg)

        try:
            self.render_page_and_broadcast_morph(reflex, selectors, data)
        except Exception as e:
            error = '{}: {}'.format(e.__class__.__name__, str(e))
            message = 'SockpuppetConsumer failed to re-render {url} {message}'.format(
                url=url, message=error
            )
            self.broadcast_error(message, data)
            raise SockpuppetError(message)
        logger.debug('Reflex took %6.2fms', (time.time() - start) * 1000)

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
                'html': ''.join([e.decode_contents() for e in document.select(selector)]),
                'children_only': True,
                'permanent_attribute_name': data['permanent_attribute_name'],
                'stimulus_reflex': {**data, 'last': selector == selectors[-1]}
            })
        channel.broadcast()

    def delegate_call_to_reflex(self, reflex, method_name, arguments):
        method = getattr(reflex, method_name)
        method_signature = inspect.signature(method)
        if len(method_signature.parameters) == 0:
            getattr(reflex, method_name)()
        else:
            getattr(reflex, method_name)(*arguments)

    def broadcast_error(self, message, data):
        channel = Channel(self.scope['session'].session_key)
        data.update({'error': 'message'})
        channel.dispatch_event({
            'name': 'stimulus-reflex:500',
            'detail': {'stimulus_reflex': data}
        })
        channel.broadcast()
