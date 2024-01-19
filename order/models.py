from django.db import models
from base.models import BaseModel
import random
from product.models import *
from account.models import *

# Create your models here.
class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField(default=100)
    minimum_amount = models.PositiveIntegerField(default=500)

    

class Order(BaseModel):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True,null=True, blank=False)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True,blank=True)
    


    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def generateTransactionId(self):
        if not self.transaction_id:
            transaction_code = random.randint(100000, 999999)
            self.transaction_id = str(transaction_code)
            self.save()
        return self.transaction_id
    
    @property
    def getCartTotal(self):
        orderitems = self.orderitem_set.all()
        total = sum(item.getTotal for item in orderitems)
        if self.coupon:
            return total - self.coupon.discount_price

        return total
    
    @property
    def getCartItems(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    
class OrderItemHistory(BaseModel):
    STATUS_TYPE = (
        ('Order Placed','Order Placed'),
        ('Order Confirmed','Order Confirmed'),
        ('Dispatched','Dispatched'),
        ('Shipped','Shipped'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
        ('Cancled','Cancled'),
        ('Return','Return'),
    )
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    color_varient = models.ForeignKey(ColorVariation,on_delete=models.SET_NULL, null = True, blank=True)
    size_varient = models.ForeignKey(SizeVariation,on_delete=models.SET_NULL, null = True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    trade_id = models.PositiveIntegerField(null=True, blank=True)
    item_price = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_TYPE,null=True, blank=True)



    class Meta:
        unique_together = (  'product', 'size_varient', 'color_varient')
        ordering = ['created']

    @property
    def generateTradeId(self):
        if not self.trade_id:
            transaction_code = random.randint(100000, 999999)
            self.trade_id = str(transaction_code)
            self.save()
        return self.trade_id
    

    @property
    def getTotal(self):
        price = [self.product.price]

        if self.color_varient:
            color_varient_price = self.color_varient.price
            price.append(color_varient_price)
        if self.size_varient:
            size_varient_price = self.size_varient.price
            price.append(size_varient_price)
        price = sum(price)
        total = price * self.quantity
        print(total)
        return total
    


    
class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    color_varient = models.ForeignKey(ColorVariation,on_delete=models.SET_NULL, null = True, blank=True)
    size_varient = models.ForeignKey(SizeVariation,on_delete=models.SET_NULL, null = True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)



    class Meta:
        unique_together = ('order', 'product', 'size_varient', 'color_varient')
    

    @property
    def getTotal(self):
        price = [self.product.price]

        if self.color_varient:
            color_varient_price = self.color_varient.price
            price.append(color_varient_price)
        if self.size_varient:
            size_varient_price = self.size_varient.price
            price.append(size_varient_price)
        price = sum(price)
        total = price * self.quantity
        print(total)
        return total
    
    
    @property
    def getProductPrice(self):
        price = [self.product.price]

        if self.color_varient:
            color_varient_price = self.color_varient.price
            price.append(color_varient_price)
        if self.size_varient:
            size_varient_price = self.size_varient.price
            price.append(size_varient_price)
        return sum(price)




class Cart(BaseModel):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="carts")
    order_items = models.ManyToManyField(OrderItem)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
   

    



  
   

