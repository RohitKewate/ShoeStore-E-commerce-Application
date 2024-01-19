from django.forms import ModelForm
from account.models import *
from django import forms

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['phone_number', 'street','city','district','state','country','pincode']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['data-placeholder'] = field.label