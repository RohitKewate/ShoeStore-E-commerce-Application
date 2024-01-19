from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name':'Name'
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs['placeholder'] = field.label


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        field = ['name','username', 'email','location','bio','profile_image']
        exclude = ['user','is_email_verified','email_token']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control single-input'})
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['onblur'] = field.label
            field.widget.attrs['onfocus'] = field.label




class AddressForm(ModelForm):
    class Meta:
        model = Address
        field = ['phone_number','street', 'city','district','state','country','pincode','default']
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['default'].widget.attrs['for'] = 'primary-checkbox'

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'single-input'})
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['onblur'] = field.label
            field.widget.attrs['onfocus'] = field.label


