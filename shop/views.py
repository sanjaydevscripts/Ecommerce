from django.shortcuts import render
from django.views import View

from shop.models import Category


class CategoryView(View):
    def get(self,request):
        c=Category.objects.all()
        return render(request,'categories.html',{'category':c})


