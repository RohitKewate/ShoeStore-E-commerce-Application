from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import *
from product.models import *
from .forms import *
from base.email import send_account_activation_email, send_welcome_email
from django.contrib.sessions.models import Session
import uuid
# Create your views here.


def loginPage(request):
    page = 'login-page'
    if request.user.is_authenticated:
        return redirect('home-page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Profile.objects.get(username=username)
        except:
            messages.error(request, "Invalid Credentials!")

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"Login Successful!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'home-page')
        else:
            return HttpResponseRedirect(request.path_info)


    context = {'page':page}
    return render(request, "account/login_registration.html",context)

def logoutPage(request):
    logout(request)
    return redirect("login-page")

def registrationPage(request):
    page='sign-up-page'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user_obj = User.objects.filter(email=user.email)
            if user_obj.exists():
                messages.warning(request, 'Email is already taken.')
                return HttpResponseRedirect(request.path_info)

            send_welcome_email(user)
            user = form.save()

            messages.success(request, "User account was created!")
            login(request,user)

            messages.success(request, "An email is sent to you!")
            return HttpResponseRedirect(request.path_info)

        else:
            messages.error(request, "Something went wrong!")


    context = {'page':page,'form':form}
    return render(request, "account/login_registration.html",context)

def activateEmail(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()

        return redirect("home-page")
    except:
        return HttpResponseRedirect("Invalid email token.")

def settingPage(request):
    user = request.user.profile

    context={'user':user}
    return render(request,"account/settings.html",context)

def editProfilePage(request):
    user = request.user.profile
    form = ProfileForm(instance=user)

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User account updated successfully!")
            return redirect('settings-page')
    

    context = {'form':form}
    return render(request,"account/profile_form.html",context)







def addressPage(request):
    user = request.user.profile
    addresses = Address.objects.filter(owner=user)
    context={'addresses':addresses}
    return render(request,"account/address.html",context)


def addAddressPage(request):
    user = request.user.profile
    form = AddressForm()

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.owner = user
            address.save()


    context = {'form':form}
    return render(request,"account/add_address.html",context)




def editAddressPage(request,pk):
    user = request.user.profile
    address = user.address_set.get(uid=pk)
    
    form = AddressForm(instance=address)
    if request.method == "POST":
        form  =AddressForm(request.POST,instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.owner = user
            address.save()
            messages.success(request, "Address updated successfully!")
            return redirect('settings-page')


    context = {'form':form}
    return render(request,"account/address_form.html",context)



def removeAddressPage(request,pk):
    page = "Remove Address"
    user = request.user.profile
    address = user.address_set.get(uid=pk)
    if request.method == "POST":
        address.delete()
        messages.success(request, 'Address Removed')
        return redirect('settings-page')

    return render(request,"account/delete_address.html")



def addWishlist(request):
    context = {}
    wishlist_form = request.POST.get("wishlist_form")
    wishlisted_products = request.session.get("wishlisted_products")
    # Initialize wishlisted_products as an empty list if it's None
    if wishlisted_products is None:
        wishlisted_products = []


    if request.method == "POST" :
        product_uid = request.POST.get('product_uid')
        try:
            unique_id = uuid.UUID(product_uid)
            unique_uid= str(unique_id)
        except ValueError:
            return render(request, 'error_template.html', {'error_message': 'Invalid UUID'})
        
        print("product wishlisted", unique_uid)
        if unique_uid not in wishlisted_products:
            wishlisted_products.insert(0,unique_uid)
            context["wishlisted_products"] = unique_uid
            request.session.save()
            messages.success(request, 'Product added to wishlist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Product is already in wishlist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def wishlistPage(request):
    context = {}
    try:
        
        sessions = Session.objects.get(session_key='wishlisted_products')
        for session in sessions:
            session_data = session.get_decoded()
            wishlisted_products = session_data.get('wishlisted_products')
            print("1:", wishlisted_products)
       
        # Initialize wishlisted_products as an empty list if it's None
        if request.session.has_key('wishlisted_products'):
            products = Product.objects.filter(uid__in=wishlisted_products)
            context["wishlisted_products"] = products
            context["has_product"] = True
            print("if:",wishlisted_products)
        
        else:
            wishlisted_products = []
            context["wishlisted_products"] = []
            context["has_product"] = False
            print("else:",wishlisted_products)
        
        print(wishlisted_products)
        return render(request,"account/user-wishlist.html",context)
    except Session.DoesNotExist:
        context = {'add_wishlist':"Add Products to your wishlist."}

        # Handle the case where the session key does not exist
        return render(request,"account/user-wishlist.html",context)


    




def contactPage(request):
    context={}
    return render(request,"account/contact.html",context)