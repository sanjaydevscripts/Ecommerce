from django.shortcuts import render,redirect
from django.views import View

from shop.models import Product

from cart.models import Cart


class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')


class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        return render(request, 'cart.html',{'cart':c})