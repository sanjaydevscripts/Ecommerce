from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from shop.models import Category,Product

from shop.forms import SignUpForm,LoginForm,AddCategoryForm,AddProductForm,AddStockForm


class Register(View):
    def get(self,request):
        form_instance=SignUpForm()
        return render(request,'register.html',{'form':form_instance})
    def post(self,request):
        form_instance=SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
class Userlogin(View):
    def get(self,request):
        form_instance=LoginForm
        return render(request,'login.html',{'form':form_instance})

    def post(self,request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            name=form_instance.cleaned_data['username']
            pwd=form_instance.cleaned_data['password']
            user=authenticate(username=name,password=pwd)#return user object if entered username and password are correct
                                                         #else returns none

            if user:    #if user exist
                login(request,user) #start new session with current user
                return redirect('shop:categories')
            else:
                # print('invalid credentials')
                messages.error(request,'Invalid credential Please Enter a valid username and password')
                return render(request,'login.html',{'form':form_instance})



class Userlogout(View):
    def get(self, request):
        logout(request)
        return redirect('shop:login')



class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'category':c})

class Productview(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        return render(request,'products.html',{'category':c})

class ProductDetail(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        return render(request, 'productdetail.html',{'product':p} )

class AddCategory(View):
    def get(self,request):
        form_instance=AddCategoryForm()
        return render(request,'addcategory.html',{'form':form_instance})
    def post(self,request):
        form_instance = AddCategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
class AddProduct(View):
    def get(self,request):
        form_instance = AddProductForm()
        return render(request, 'addproduct.html', {'form': form_instance})
    def post(self,request):
        form_instance = AddProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

class AddStock(View):
    def get(self,request,i):
        p=Product.objects.get(id=1)
        form_instance = AddStockForm(instance=p)
        return render(request, 'addstock.html', {'form': form_instance})
    def post(self,request,i):
        p = Product.objects.get(id=1)
        form_instance = AddStockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')






