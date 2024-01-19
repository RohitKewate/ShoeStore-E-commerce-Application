from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50, null=True,blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profiles", default="profiles/avatar.svg")

    
    def __str__(self):
        return str(self.name)


class Address(BaseModel):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    phone_number = PhoneNumberField(null=True,blank=True)
    street = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    district = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.PositiveIntegerField()
    default = models.BooleanField(default=False)


    def __str__(self):
        return str(self.city)
    
  

