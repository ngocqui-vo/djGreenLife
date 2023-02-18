from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


class CustomerCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name']


class SignUpForm(UserCreationForm):
    # customer = CustomerCreationForm()
    # first_name = forms.CharField(max_length=30, required=True)
    # last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
