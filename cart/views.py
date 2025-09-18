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

class DecrementQuantity(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        c=Cart.objects.get(user=u,product=p)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.quantity=1
        return redirect('cart:cartview')

class DeleteItem(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        c=Cart.objects.get(user=u,product=p)
        c.delete()
        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        for i in c:
            total=i.quantity*i.product.price

        return render(request, 'cart.html',{'cart':c,'total':total})


class CheckOut(View):
    def get(self,request):
        return render(request,'checkout.html')