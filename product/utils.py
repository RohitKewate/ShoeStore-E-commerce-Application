from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *



def paginateProduct(request, products, results):

    page = request.GET.get('page')
    paginator =Paginator(products, results)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)
    
    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1
    

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex,rightIndex)


    return custom_range , products



def searchProducts(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')


    category = Category.objects.filter(category_name__icontains = search_query)

    products = Product.objects.distinct().filter(
        Q(product_name__icontains = search_query) |
        Q(product_description__icontains = search_query) |
        Q(brand__brand_name__icontains = search_query) |
        Q(category__in = category)

    )
    return products, search_query