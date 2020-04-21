import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


logger = logging.getLogger('sockpuppet')


class SockpuppetConsumer(JsonWebsocketConsumer):
    channel_name = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('initialize')
        logger.info('test info')
        self.subscriptions = set()

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

