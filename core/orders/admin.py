from django.contrib import admin

# Register your models here.



from .models import Menu, Order, WalletMoney


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'menu', 'quantity', 'total_price', 'order_status')
    search_fields = ('order_id',)
    list_filter = ('order_status',)


class WalletMoneyAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
    search_fields = ('user__username',)


admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(WalletMoney, WalletMoneyAdmin)
