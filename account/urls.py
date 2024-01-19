from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("login/",views.loginPage, name="login-page" ),
    path("logout/",views.logoutPage, name="logout-page" ),
    path("sign-up/",views.registrationPage, name="sign-up-page" ),
    path("settings/",views.settingPage, name="settings-page" ),
    path("edit-profile/",views.editProfilePage, name="edit-profile-page" ),
    path("add-address/",views.addAddressPage, name="add-address-page" ),
    path("edit-address/<str:pk>/",views.editAddressPage, name="edit-address-page" ),
    path("remove-address/<str:pk>/",views.removeAddressPage, name="remove-address-page" ),
    path("address/",views.addressPage, name="address-page" ),
    path("contact/",views.contactPage, name="contact-page" ),
    path("activate/<email_token>",views.activateEmail, name="activate-page" ),
    path("wishlist/",views.wishlistPage, name="wishlist-page" ),
    path("add-to-wishlist/",views.addWishlist, name="add_to_wishlist" ),
]
