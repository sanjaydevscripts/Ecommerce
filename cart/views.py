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


from cart.forms import OrderForm

def check_stock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
        else:
            stock=True
    return stock


import razorpay
class CheckOut(View):
    def get(self,request):
        form_instance=OrderForm()
        return render(request,'checkout.html',{'form':form_instance})

    def post(self, request):
        form_instance = OrderForm(request.POST)
        u=request.user
        if form_instance.is_valid():
            # data=form_instance.cleaned_data
            # print(data)
            o=form_instance.save(commit=False)
            o.user=u
            o.save()

            c=Cart.objects.filter(user=u)
            stock = check_stock(c)
            if stock:
                total=0
                for i in c:
                    total+=i.quantity * i.product.price

                if o.payment_method=="online":
                    # rezopay client connection
                    client=razorpay.Client(auth=('rzp_test_RJOTa18jmnSyYc','jC1EgRTw7Na85oUrC2yvNESQ'))
                    #replace order
                    response_payment=client.order.create(dict(amount=total,currency='INR'))
                    print(response_payment)
                    order_id=response_payment['id']
                    o.order_id=order_id
                    o.amount=total
                    o.save()
                    return render(request,'payment.html')
                else:
                    pass
            else:
                print("Items not available")

            return render(request, 'checkout.html', {'form': OrderForm()})


