from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Category, Product, Customer


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
        else:
            messages.error(request, 'user or password is invalid!!!')
    return render(request, 'store/signin.html', {})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        is_male = request.POST['is_male']
        username = request.POST['username']
        password = request.POST['password']
        user, created = User.objects.get_or_create(username=username)
        if created:
            customer = Customer.objects.create(first_name=first_name, last_name=last_name, is_male=is_male)
            user.password = password
            user.save()
            customer.user = user
            return redirect('store:user_login')
        else:
            messages.error(request, 'user already exist!!!')
    return render(request, 'store/register.html', {})


def user_logout(request):
    logout(request)
    return redirect('store:user_login')
