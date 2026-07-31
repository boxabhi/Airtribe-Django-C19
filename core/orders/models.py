from django.db import models
from utility.models import BaseModel
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync,sync_to_async



class Menu(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_id = models.CharField(max_length=100,null=True, blank=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    order_status = models.CharField(max_length=20, choices = (
        ("CREATED", "Created"),
        ("PREPARING", "Preparing"),
        ("BAKING", "Baking"),
        ("BAKED", "Baked"),
        ("DELIVERING", "Delivering"),
        ("DELIVERED", "Delivered"),
        ), default="CREATED")


    def __str__(self):
        return f"Order of {self.quantity} x {self.menu.name}"



@receiver(post_save, sender=Order)
def create_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        today = datetime.now().strftime("%Y%m%d")
        instance.order_id = f"OD{today}{instance.id}"
        instance.save()

    payload = {
        "order_status" : instance.order_status,
        "order_id" : instance.order_id,
        "progress" : 10
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{instance.order_id}",
        {
            "type": "order_status_update",
            "message": json.dumps(payload)
        }
    )
    print("CHANNLE INFORMATION SENT")


class WalletMoney(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"WalletMoney - {self.user.username} | Amount : {self.amount}"

