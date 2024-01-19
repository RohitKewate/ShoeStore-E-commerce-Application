from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from account.models import Profile
from django.db.models import F, Q, Count, Sum, ExpressionWrapper, IntegerField




# Create your models here.
class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self,*args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.category_name)
    
    @property
    def get_category_product_count(self):
        return self.category.count()


class Brand(BaseModel):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    brand_image = models.ImageField(upload_to="brand", null=True, blank=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.brand_name)
    
    @property
    def get_brand_product_count(self):
        return self.brand.count()
    

class ColorVariation(BaseModel):
    color_name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.color_name)
    
    def get_color_product_count(self, color_name):
        return self.product.filter(color_variation__color_name=color_name).count()


class SizeVariation(BaseModel):
    size_name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.size_name)




class Product(BaseModel):
    QUANTITY_TYPE = (
        ('In Stock','In Stock'),
        ('Only few Left!','Only few Left!'),
    )

    TAG_TYPE = (
        ('New','New'),
        ('Trending','Trending'),
        ('On Sale','On Sale'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, auto_created=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    mrp_price = models.IntegerField(null=True, blank=True)
    price = models.IntegerField()
    rate_count = models.PositiveIntegerField(null=True,blank=True)
    overall_rate = models.PositiveIntegerField(null=True,blank=True)
    product_intro = models.TextField(max_length=500,null=True, blank=True)
    product_description = models.TextField(max_length=500,null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand",null=True, blank=True)
    color_variation = models.ManyToManyField(ColorVariation,default=None)
    size_variation = models.ManyToManyField(SizeVariation,default=None)
    gender_available = models.CharField(max_length=50,choices=GENDER_CHOICES,null=True, blank=True)
    availability = models.CharField(max_length=50,choices=QUANTITY_TYPE,null=True, blank=True)
    tag = models.CharField(max_length=50,choices=TAG_TYPE,null=True, blank=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    

    class Meta:
        ordering = ['-overall_rate', 'product_name']

    def __str__(self):
        return str(self.product_name)
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__uid',flat=True)
        return queryset
    
    def getProductPriceByColor(self,color):
        return self.price + ColorVariation.objects.get(color_name =color).price
    
    def getProductPriceBySizeAndColor(self,size,color):
        return self.price + ColorVariation.objects.get(color_name =color).price + SizeVariation.objects.get(size_name =size).price
    

    @property
    def getOverallRating(self):
        # Annotate the QuerySet with the count of ratings for each value
        products = Product.objects.filter(uid=self.uid)
        reviews = self.review_set.all()
        # Calculate the overall rating using the aggregate data
        total_rating_1 = reviews.filter(value="1").count()
        total_rating_2 = reviews.filter(value="2").count()
        total_rating_3 = reviews.filter(value="3").count()
        total_rating_4 = reviews.filter(value="4").count()
        total_rating_5 = reviews.filter(value="5").count()
        total_ratings = self.review_set.count()
        
        if total_ratings > 0 and total_ratings != None:
            overall_rating = ( (1 * total_rating_1) + (2 * total_rating_2) + (3 * total_rating_3) + (4 * total_rating_4) + (5 * total_rating_5)) / total_ratings
                # ... repeat for each rating value
              
        else:
            overall_rating = 0

        self.overall_rate = overall_rating
        self.rate_count = total_ratings
        self.save()
        return overall_rating
        

     
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Specifications(BaseModel):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    material = models.CharField(max_length=50,null=True, blank=True)
    Ankle_height = models.CharField(max_length=50,null=True, blank=True, default=None)
    sport = models.CharField(max_length=50,null=True, blank=True, default=None)
    fastening = models.CharField(max_length=50,null=True, blank=True, default=None)
    outsole_Type = models.CharField(max_length=50,null=True, blank=True, default=None)
    arch_type = models.CharField(max_length=50,null=True, blank=True, default=None)
    running_type = models.CharField(max_length=50,null=True, blank=True, default=None)
    surface_type = models.CharField(max_length=50,null=True, blank=True, default=None)

    def __str__(self):
        return str(self.product.product_name) + "Specifications"



class Review(BaseModel):
    RATE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=1,choices=RATE)
   
    class Meta:
        unique_together = [['owner', 'product']]

    def __str__(self):
        return self.value


class Comment(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()  

    def __str__(self):
        return self.content