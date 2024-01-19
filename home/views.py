from django.shortcuts import render
from order.models import *
from product.models import *
from django.http import JsonResponse
import json


# Create your views here.
def homePage(request):
    products = Product.objects.all()



    context={'products': products}
    return render(request,"home/home.html",context)