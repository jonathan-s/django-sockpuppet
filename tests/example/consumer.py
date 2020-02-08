import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.__class__.__name__,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.__class__.__name__,
            self.channel_name
        )

        # Receive message from room group
    def message(self, event):
        # Send message to WebSocket
        print('something')
        self.send(text_data=json.dumps(event))

    def receive(self, text_data):
        '''
        need a way to identify the correct consumer...
        {
            "target": "TodosReflex#create",
            "args": [],
            "url": "http://localhost:3000/demos/todo",
            "attrs": {
                "autofocus": "",
                "class": "new-todo",
                "placeholder": "What needs to be done?",
                "data-target": "todos.input",
                "data-reflex": "change->TodosReflex#create",
                "data-action": "change->todos#__perform",
                "data-reflex-permanent": "",
                "value": "this",
                "checked": false,
                "selected": false
            },
            "selectors": [],
            "permanent_attribute_name": "data-reflex-permanent"
        }
        '''

        print('nothing should happen here', text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
