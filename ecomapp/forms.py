from dataclasses import field
from django import forms
from .models import Customer, Order, Product
from django.contrib.auth.models import User

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', "address"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Customer with this username already exists')

        return username

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "slug", "category", "image", "marked_price", "selling_price", "description", "warranty", "return_policy"]


        #for designing th form
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the Book Title"
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter a unique slug for your book."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form.control"
            }),
            "marked_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product"
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Book Decription",
                "rows": 5
            }),
            "warranty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Is there a warranty?"
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the return policy for the book."
            }),
        }