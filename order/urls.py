
from django.urls import path
from . import views


urlpatterns = [
    path("cart/",views.cartPage, name="cart-page" ),
    path("add-to-cart/<str:uid>/",views.addToCartPage, name="add_to_cart" ),
    path("checkout/",views.checkoutPage, name="checkout-page" ),
    path("remove-coupon/<str:uid>/",views.removeCoupon, name="remove_coupon" ),
    path("success/",views.successPage, name="success" ),
    path("your-order/",views.yourOrderPage, name="your-order-page" ),
    
]