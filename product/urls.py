from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("shop/",views.productsPage, name="products-page" ),
    path("<slug:slug>/",views.productDetailPage, name="product-details-page" ),
    
]
