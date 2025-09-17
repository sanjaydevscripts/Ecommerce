from django.contrib.auth.models import User
from django.db import models

from shop.models import Product


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def subtotal(self):
        return self.quantity * self.product.price