from django.shortcuts import render,HttpResponseRedirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import F
from .forms import AddressForm
import razorpay
from django.conf import settings

# Create your views here.




def addToCartPage(request, uid):

    try:
        product =Product.objects.get(uid=uid)
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        cart, created = Cart.objects.get_or_create(user=customer)
        
        
        size_variation = None
        if request.session.get('size'):
            size = request.session.get('size')
            size_variation = SizeVariation.objects.get(size_name=size)
            
        color_variation = None   
        if request.GET.get('color'):
            color = request.GET.get('color')
            color_variation = ColorVariation.objects.get(color_name=color)
            

                # Update or create the OrderItem
        orderItem, created = OrderItem.objects.update_or_create(
            order=order,
            product=product,
            size_varient=size_variation,
            color_varient=color_variation,
            defaults={'quantity': 1}  # Set the default value of quantity to 1
        )

       

        if created:
            orderItem.quantity = 1
            orderItem.save()
        # Check if the OrderItem already exists and update the quantity
        elif OrderItem.objects.filter(product=product, color_varient=color_variation, size_varient=size_variation).exists():
            # Increment the quantity using F expression
            OrderItem.objects.filter(product=product, color_varient=color_variation, size_varient=size_variation).update(quantity=F('quantity') + 1)


        messages.success(request,"Product added to cart.")
        

    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    except SizeVariation.DoesNotExist:
        messages.error(request, "Please select a valid size.")
    except ColorVariation.DoesNotExist:
        messages.error(request, "Please select a valid color.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cartPage(request):
    total_price = 0 
    try:
        total_price = 0  # Initialize total_price outside the conditional block
        if request.user.is_authenticated:
            customer = request.user.profile
            order, created = Order.objects.get_or_create(customer=customer, complete =False)
            order.generateTransactionId
            items = order.orderitem_set.all()

            # Create a Cart model if it doesn't exist for the user
            cart = Cart.objects.get(user=customer)
            
            try:
                product_id = request.POST.get('productid')
                add = request.POST.get('add')
                sub = request.POST.get('sub')
                color = request.POST.get('color')
                size = request.POST.get('size')


                if product_id is not None:  # Check if product_id is provided in POST data
                    product = Product.objects.get(uid=product_id)

                    # Ensure color and size is not None and it represents a valid color and size name
                    if color and size:
                        color_variation = ColorVariation.objects.get(color_name=color)
                        size_variation = SizeVariation.objects.get(size_name=size)
                        item = OrderItem.objects.get(order=order, product=product, color_varient=color_variation, size_varient=size_variation)

                        if sub:
                            item.quantity -= 1
                            item.save()

                        elif add:
                            item.quantity += 1
                            item.save()

                        if item.quantity == 0:
                            item.delete()

                    else:
                        messages.error(request, "Something went wrong!")
                
            

            except Product.DoesNotExist:
                messages.error(request, "Invalid product ID.")
            except OrderItem.DoesNotExist:
                messages.error(request, "OrderItem not found.")
            except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                
            try:
                if request.method == "POST" and 'coupon' in request.POST:
                    coupon = request.POST.get('coupon')
                    couponObj = Coupon.objects.get(coupon_code__icontains= coupon)
                    if not couponObj:
                        messages.info(request, "Invalid Coupon.")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    if order.coupon:
                         if order.coupon == couponObj:
                            messages.info(request, "Coupon already applied.")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                         else:
                            messages.info(request, "Another coupon already exists.")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    if order.getCartTotal < couponObj.minimum_amount:
                        messages.info(request, f"Amount should be greater than {couponObj.minimum_amount}.")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    if couponObj.is_expired:
                        messages.info(request, "Coupon is expired")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
                    

                    order.coupon = couponObj
                    order.save()

                    
            
                    print("DEBUG: order.getCartTotal()", order.getCartTotal)
                    print("DEBUG: order.coupon.discount_price", order.coupon.discount_price)
                    print("DEBUG: total_price", total_price)
                    messages.success(request, "Coupon Applied.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    total_price = order.getCartTotal
                    print("DEBUG1: total_price", total_price)
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

            context ={'items':items,'order':order}
        else:
            items = []
            order = None
            total_price = order.getCartTotal
            print("DEBUG: total_price", total_price)
            context ={'items':items, 'order':order}
    except:
        items = None
        order = None
        print("DEBUG: total_price", total_price)
        context ={'items':items, 'order':order}

    return render(request,"order/cart.html", context) 



def removeCoupon(request,uid):
    print(uid)
    try:
        order = get_object_or_404(Order, uid=uid)
        
        if order.coupon:
            order.coupon = None
            order.save()
            messages.success(request, "Coupon Removed.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def checkoutPage(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete =False)
        items = order.orderitem_set.all()
        cart, cart_created = Cart.objects.get_or_create(user=customer, is_paid=False)
        addresses = customer.address_set.all()
        selected_address_id = request.POST.get('selected_address')
        save_address = request.POST.get('save_address')

        if selected_address_id:
            selected_address = Address.objects.filter(uid=selected_address_id, owner=customer).first()
            if selected_address:
                form = AddressForm(instance=selected_address)
            else:
                messages.error(request, "Selected address not found.")
                form = AddressForm()
        elif save_address:
            form = AddressForm(request.POST)
            if form.is_valid():
                address_instance = form.save(commit=False)
                address_instance.owner = customer
                address_instance.default = True
                address_instance.save()
                messages.success(request, "Address updated successfully.")
            else:
                messages.error(request, "Please fill the address details correctly.")
        else:
            form = AddressForm()


        if cart:
            client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            payment = client.order.create({'amount' : order.getCartTotal*100, 'currency' : 'INR', 'payment_capture': 1 })
            print(payment)
            cart.razorpay_order_id = payment['id']
            cart.save()
        else:
            payment = None
            
        

        


    context ={'items':items,'order':order,'form':form, 'payment':payment,'addresses':addresses}
    return render(request,"order/checkout.html", context)


def successPage(request):

    if request.user.is_authenticated:
        order_id = request.GET.get('razorpay_order_id')
        customer = request.user.profile
        cart = Cart.objects.get(user=customer,razorpay_order_id = order_id)
        cart.is_paid = True
        cart.save()
        trade_id = 0
        
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()

        total_price = order.getCartTotal
        address = Address.objects.filter(owner=customer, default=True)[0]
        for item in items:
            product = item.product
            size_variation = item.size_varient
            color_variation = item.color_varient
            quantity = item.quantity
            item_price = item.getProductPrice
            print("item_price:",item_price)


            orderItemHistory, created = OrderItemHistory.objects.update_or_create(
                customer=customer,
                product=product,
                size_varient=size_variation,
                color_varient=color_variation,
                quantity=quantity,
                item_price=item_price,
                status = "Order Placed"
            )
            trade_id = orderItemHistory.generateTradeId
            
        
    context ={'order':order,'total_price':total_price,'items':items,'trade_id':trade_id,'address':address}
    return render(request,"order/success.html", context)




def yourOrderPage(request):
    customer = request.user.profile
    try:
        order_items = OrderItemHistory.objects.filter(customer=customer)
        
                
    except:
        messages.error(request, "Couldn't fetch your orders.")

    context={'order_items':order_items}
    return render(request,"order/your_order.html", context)
