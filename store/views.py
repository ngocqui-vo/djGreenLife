from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

from .models import Category, Product, Customer
from .forms import SignUpForm


def home(request):
    products = Product.objects.all().order_by('-created')[:7]
    context = {'products': products}
    return render(request, 'store/index.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    return render(request, 'store/product-detail.html', context)


def category_products(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products = category.products.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'User or password is invalid!!!')
            return redirect('store:user_login')
    return render(request, 'store/signin.html', {})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        forms = SignUpForm(request.POST)

        if forms.is_valid():
            user = forms.save()
            first_name = forms.cleaned_data.get('first_name')
            last_name = forms.cleaned_data.get('last_name')
            is_male = bool(int(request.POST['is_male']))
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, user=user, is_male=is_male)
            customer.save()
            return redirect('store:user_login')
        else:
            messages.error(request, 'User already exist!!!')
            return redirect('store:user_register')
    else:
        forms = SignUpForm()
    return render(request, 'store/register.html', {'forms': forms})


def user_logout(request):
    logout(request)
    return redirect('store:user_login')
