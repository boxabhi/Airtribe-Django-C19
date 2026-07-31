from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from orders.models import Order, WalletMoney

# Create your views here.



def orders_view(request, order_id):
    order = Order.objects.get(order_id=order_id)
    return render(request, 'order.html', {"order": order})



def wallet_view(request):
    with transaction.atomic():
        wallet_abhijeet = WalletMoney.objects.get(user__username='abhijeet')
        wallet_rahul = WalletMoney.objects.get(user__username='Rahul')

        wallet_abhijeet.amount -= 500
        wallet_rahul.amount += 500
        wallet_abhijeet.save()

        raise Exception("Intentional Exception for Testing")  # This will raise an exception before saving Rahul's wallet
        wallet_rahul.save()
        
        return HttpResponse(f"Wallet updated successfully. New balances: Abhijeet - {wallet_abhijeet.amount}, Rahul - {wallet_rahul.amount}")

    return HttpResponse("An error occurred while updating the wallet. Transaction rolled back.")