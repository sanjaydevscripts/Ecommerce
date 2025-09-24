from django.contrib import admin

from cart.models import Cart,Order_items,Order

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_items)
