from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from order.models import *
from .forms import CommentForm
from django.db.models import Q
from django.contrib import messages
from .utils import searchProducts,paginateProduct

# Create your views here.

def productsPage(request):
    categories = Category.objects.all()
    sizes = SizeVariation.objects.all()
    colors = ColorVariation.objects.all()
    brands = Brand.objects.all()
    tag = request.GET.get("tag")
    search_input =request.GET.get("search_input")
    check_filter =request.GET.get("check_filter")
    brand_filter = request.GET.getlist('brand') if request.GET.getlist('brand_filter') != None else ''
    color_filter = request.GET.getlist('color') if request.GET.getlist('color_filter') != None else ''
    size_filter = request.GET.getlist('size') if request.GET.getlist('size_filter') != None else ''

    q = request.GET.get('q') if request.GET.get('q') != None else ''  # Get the 'q' parameter from the URL
    
    

    if q:
        products = Product.objects.distinct().filter(
            Q(category__category_name__icontains=q) |
            Q(brand__brand_name__in=brand_filter) |
            Q(color_variation__color_name__in=color_filter) |
            Q(size_variation__size_name__in=size_filter)
            
        )
        print("if",products)

        

    else:
        products = Product.objects.all()
        print("else",products)
    
    if tag:
        tag_value = request.GET.get("tag_value")
        products = Product.objects.filter(tag = tag_value)

    if check_filter:
            print("brand",brand_filter)
            print("color",color_filter)
            print("size",size_filter)
    
            products = Product.objects.distinct().filter(
                Q(brand__brand_name__in=brand_filter) |
                Q(color_variation__color_name__in=color_filter) |
                Q(size_variation__size_name__in=size_filter)
                )
            
    search_query = ''
    if search_input:
        products, search_query = searchProducts(request)   
   
    custom_range, products = paginateProduct(request, products, 6)

    color_counts = {}  # Create a dictionary to hold color counts

    for color in colors:
        color_counts[color.color_name] = Product.objects.filter(color_variation__color_name=color.color_name).count()
    

    size_counts = {}  # Create a dictionary to hold color counts

    for size in sizes:
        size_counts[size.size_name] = Product.objects.filter(size_variation__size_name=size.size_name).count()

    context = {'products':products,'custom_range': custom_range,'search_query': search_query,'categories':categories,'brands':brands,'sizes':sizes,'size_counts': size_counts,'colors':colors, 'color_counts': color_counts}
    return render(request,"product/shop.html", context)


def productDetailPage(request,slug):
    context={}

    product = get_object_or_404(Product, slug=slug)
    specifications = Specifications.objects.get(product=product)
    context = {'product':product,'specifications':specifications}



    
    if request.GET.get('color'):
        color = request.GET.get('color')
        colorprice = product.getProductPriceByColor(color)
        context['selected_color'] = color
        context['updated_price'] = colorprice
        
    
        if request.method == 'POST':
            size = request.POST.get('size')
            price = product.getProductPriceBySizeAndColor(size,color)
            request.session['size'] = size
            context['selected_size'] = size
            context['updated_price'] = price
        else:
            context['updated_price'] = colorprice
    

    customer = request.user.profile
    

    # Review functionality
    rate = request.POST.get('rate')
    # Convert None to a character, e.g., 'N'
    if rate is None:
        rate = 'N'
    
    if customer.uid not in product.reviewers:
        if request.method == "POST" and rate:
            if request.user.is_authenticated:
                review = request.POST.get('review')
                print("if",review)
                review_object= Review.objects.create(
                    owner =customer,
                    product=product,
                    body=review,
                    value = rate,
                )

    # comment functionality
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = customer
            comment.product = product
            comment.save()
    
    products = Product.objects.all()
    comments = Comment.objects.filter(product=product)
    context['form'] = form
    context['comments'] = comments
    context['products'] = products
   

    
    return render(request,"product/product-details.html",context)







