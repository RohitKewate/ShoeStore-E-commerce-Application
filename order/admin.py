from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'color_varient','size_varient']


class OrderItemHistoryAdmin(admin.ModelAdmin):
    list_display = ['trade_id','product', 'quantity', 'color_varient','size_varient',]


admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Cart)
admin.site.register(OrderItem,OrderAdmin)
admin.site.register(OrderItemHistory,OrderItemHistoryAdmin)
