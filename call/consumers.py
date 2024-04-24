# server-side consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class CallConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("WebSocket connected")

    def disconnect(self, close_code):
        if hasattr(self, 'my_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.my_name,
                self.channel_name
            )
        print("WebSocket disconnected")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("Received message:", text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']
            self.my_name = name.split('@')[0]  # Simplified group name (username)
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )
            print(f"{self.my_name} logged in and joined group {self.my_name}")

        elif eventType == 'call':
            name = text_data_json['data']['name']
            rtc_message = text_data_json['data']['rtcMessage']
            print(f"{self.my_name} is calling {name}")
            self.send_call(name, rtc_message)

        elif eventType == 'answer_call':
            caller = text_data_json['data']['caller']
            rtc_message = text_data_json['data']['rtcMessage']
            print(f"{self.my_name} is answering {caller}'s call.")
            self.send_answer(caller, rtc_message)

    def send_call(self, recipient, rtc_message):
        print(f"Sending call to {recipient} with message: {rtc_message}")
        if self.group_exists(recipient):
            async_to_sync(self.channel_layer.group_send)(
                recipient,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': rtc_message
                    }
                }
            )
        else:
            print(f"Recipient group {recipient} does not exist.")

    def send_answer(self, caller, rtc_message):
        print(f"Sending answer to {caller} with message: {rtc_message}")
        if self.group_exists(caller):
            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': rtc_message
                    }
                }
            )
        else:
            print(f"Caller group {caller} does not exist.")

    def group_exists(self, group_name):
        return async_to_sync(self.channel_layer.group_contains)(group_name, self.channel_name)
