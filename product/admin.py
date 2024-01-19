from django.contrib import admin
from .models import *

# Register your models here.



class ProductImageAdmin(admin.StackedInline):
    model = ProductImage 

class SpecificationsAdmin(admin.StackedInline):
    model = Specifications 


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    prepopulated_fields = {"slug":("product_name",)}
    inlines = [ProductImageAdmin, SpecificationsAdmin] 


@admin.register(ColorVariation)
class ColorVariationAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariation


@admin.register(SizeVariation)
class SizeVariationAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariation


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Specifications)





