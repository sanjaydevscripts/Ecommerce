
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View

from shop.models import Product

from cart.models import Cart,Order_items




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

from django.contrib import messages
import razorpay
class CheckOut(View):
    def get(self,request):
        form_instance=OrderForm()
        return render(request,'checkout.html',{'form':form_instance})

    def post(self, request):
        u = request.user
        c = Cart.objects.filter(user=u)
        stock = check_stock(c)
        if stock:
            form_instance = OrderForm(request.POST)

            if form_instance.is_valid():
                # data=form_instance.cleaned_data
                # print(data)
                o=form_instance.save(commit=False)
                o.user=u
                o.save()


                total=0
                for i in c:
                    total+=i.quantity * i.product.price

                for i in c:
                    order=Order_items.objects.create(order=o,product=i.product,quantity=i.quantity)
                    order.save()

                if o.payment_method=="online":
                    # rezopay client connection
                    client=razorpay.Client(auth=('rzp_test_RJOTa18jmnSyYc','jC1EgRTw7Na85oUrC2yvNESQ'))
                    #replace order
                    response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                    print(response_payment)
                    order_id=response_payment['id']
                    o.order_id=order_id
                    o.amount=total
                    o.save()
                    return render(request,'payment.html',{'payment':response_payment})
                elif o.payment_method=='COD':
                    o.is_ordered=True
                    o.amount=total
                    o.save()

                    items=Order_items.objects.filter(order=o)
                    for i in items:
                        i.product.stock -= i.quantity
                        i.product.save()
                    c.delete()
                    return redirect('shop:categories')

        else:
                messages.error(request,"Currently Items not available")
                print("Items not available")
                return render(request,'payment.html')

from django.views.decorators.csrf import csrf_exempt
from cart.models import Order
from django.contrib.auth import login
from django.contrib.auth.models import User

@method_decorator(csrf_exempt,name="dispatch")
class PaymentSuccess(View):
    def post(self,request,i):

        u=User.objects.get(username=i)
        login(request,u)

        response = request.POST #order_id,razorpay payment_id,razorpay_signature
        print(response)
        # to change the ordered status to true
        # first retrieve the order object whose order_id matches with response order id
        id = response['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()

        #To reduce the stock
        items = Order_items.objects.filter(order=o)
        for i in items:
            i.product.stock -= i.quantity
            i.product.save()


        c=Cart.objects.filter(user=u)
        c.delete()

        return render(request,'payment_sucess.html')

class OrderSummery(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        return render(request,'yourorders.html',{'orders':o})


