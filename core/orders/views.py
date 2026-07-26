from django.shortcuts import render

from orders.models import Order

# Create your views here.



def orders_view(request, order_id):
    order = Order.objects.get(order_id=order_id)
    return render(request, 'order.html', {"order": order})