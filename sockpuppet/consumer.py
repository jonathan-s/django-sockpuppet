
import logging
from importlib import import_module
from os import walk

from django.apps import apps
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


logger = logging.getLogger('sockpuppet')


'''
how to send to a specific group.

deal with that a bit later.
'''


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

    def disconnect(self):
        super().disconnect()
        session = self.scope['session']
        async_to_sync(self.channel_layer.group_discard)(
            session.session_key,
            self.channel_name
        )
        logger.debug(
            ':: DISCONNECT: Channel %s session: %s',
            self.channel_name, session.session_key
        )

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

    def receive_json(self, content, **kwargs):
        logger.debug('Json: %s', content)
        logger.debug('kwargs: %s', kwargs)
