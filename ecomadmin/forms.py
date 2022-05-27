from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from .models import Admin

class AdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter a username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter a Password"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email address"
    }))
    class Meta:
        model = Admin
        fields = ['full_name', 'image', 'mobile']
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Store Name"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form.control"
            }),
            "mobile": forms.NumberInput(attrs={
                "class": "form.control",
                "placeholder": "Enter your phone number"
            })

        }