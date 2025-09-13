from django.shortcuts import render
from django.views import View

from shop.models import Category


class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'category':c})

class Product(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        return render(request,'products.html',{'category':c})



