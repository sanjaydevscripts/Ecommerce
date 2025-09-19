from cart.models import Order
from django import forms


class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('online','online'),
        ('COD','COD'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
    )

    class Meta:
        model=Order
        fields=['address','phone','payment_method']