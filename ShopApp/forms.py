from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from ShopApp.models import Product


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProductForm(forms.ModelForm):

    title = forms.CharField(label='Product title')

    class Meta:
        model = Product
        fields = '__all__'

        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
