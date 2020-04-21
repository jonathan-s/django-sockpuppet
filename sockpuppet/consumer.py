
import logging
from importlib import import_module
from os import walk

from django.apps import apps
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


logger = logging.getLogger('sockpuppet')


class SockpuppetConsumer(JsonWebsocketConsumer):
    channel_name = ''
    reflexes = {}

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriptions = set()

        if not self.reflexes:
            configs = apps.app_configs.values()
            for config in configs:
                self.load_reflexes_from_config(config)

    def receive_json(self, content, **kwargs):
        logger.debug('Json: %s', content)
        logger.debug('kwargs: %s', kwargs)

    def subscribe(self, event):
        room_name = event['room_name']
        if room_name not in self.subscriptions:
            logger.debug(f':: SUBSCRIBE {self.channel_name} {room_name}')
            async_to_sync(self.channel_layer.group_add)(
                room_name,
                self.channel_name
            )
            self.subscriptions.add(room_name)

    def unsubscribe(self, event):
        room_name = event['room_name']
        if room_name in self.subscriptions:
            logger.debug(f':: UNSUBSCRIBE {self.channel_name} {room_name}')
            async_to_sync(self.channel_layer.group_discard)(
                room_name,
                self.channel_name
            )
            self.subscriptions.discard(room_name)

    def connect(self):
        super().connect()
        self.scope['channel_name'] = self.channel_name
        # self.send_json({
        #     'type': 'components',
        #     'component_types': {
        #         name: c.extends for name, c in Component._all.items()
        #     }
        # })
        logger.debug(f':: CONNECT {self.channel_name}')

    def disconnect(self, close_code):
        for room in list(self.subscriptions):
            self.unsubscribe({'room_name': room})
        logger.debug(f':: DISCONNECT {self.channel_name}')
