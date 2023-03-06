from django import forms
from .models import ProductModel

class AddProductForm(forms.ModelForm):
    class Meta:
        model=ProductModel
        fields = ('name','full_name','des','all_price','off_price')
