from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async

from orders.models import Order
import json



class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = f'order_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        order = Order.objects.filter(order_id=self.room_name)
        if not order.exists():
            self.close()

        self.accept()
        self.send(text_data=json.dumps({
            "message": f"Connected to order {self.room_name}",
            "status" : True
        }))


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json["message"], type(text_data_json["message"]))
        print(text_data_json["message"] == "Hi")
        if text_data_json["message"] == "Hi":
            self.send(text_data=json.dumps({
                "message": f"Hello! How can I help you today?",
                "status" : True
            }))
            return

        order = Order.objects.get(order_id=self.room_name)
        self.send(text_data=json.dumps({
            "message": f"Your order is in {order.order_status} status. It will be delivered soon.",
            "status" : True
        }))

    def order_status_update(self, event):
        print("*********")
        print(event)
        print("*********")
        data = json.loads(event['message'])
        self.send(text_data=json.dumps({
            "payload" : data,
        }))


class JobConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['job_id']
        self.room_group_name = f'job_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name 
        )
        self.accept()
        self.send(text_data=json.dumps({
            "message": f"Connected to job {self.room_name}",
            "status" : True
        }))


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json["message"], type(text_data_json["message"]))
        print(text_data_json["message"] == "Hi")
        if text_data_json["message"] == "Hi":
            self.send(text_data=json.dumps({
                "message": f"Hello! How can I help you today?",
                "status" : True
            }))
            return


    def send_person_event(self, event):
        print("*********")
        print(event)
        print("*********")
        data = json.loads(event['message'])
        self.send(text_data=json.dumps({
            "payload" : data,
        }))