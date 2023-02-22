import json
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse

from .models import Category, Product, Customer, Order, OrderItem
from .forms import SignUpForm


def home(request):
    products = Product.objects.all().order_by('-created')[:8]
    context = {'products': products}
    return render(request, 'store/index.html', context)


def search_products(request):
    query = request.GET.get('q')
    if query is not None:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    if page is None:
        page = 1
    items = paginator.get_page(page)
    context = {
        'products': items,
        'query': query
    }
    return render(request, 'store/store.html', context)


# def all_products(request):
#     products = Product.objects.all().order_by('-created')
#     context = {'products': products}
#     return render(request, 'store/store.html', context)


def category_products(request, slug):
    category = Category.objects.get(slug=slug)
    products = category.products.all()
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    if page is None:
        page = 1
    items = paginator.get_page(page)
    context = {
        'category': category,
        'products': items
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    return render(request, 'store/product-detail.html', context)


@login_required(login_url='/login/')
def cart(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer)

    context = {
        'items': order.order_items.all(),
        'order': order
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='/login/')
def place_order(request):
    customer = request.user.customer
    order = Order.objects.get(customer=customer)

    context = {
        'items': order.order_items.all(),
        'order': order
    }
    return render(request, 'store/place-order.html', context)


@csrf_exempt
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        action = data['action']
        print(data)
        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            order_item.quantity += 1
        elif action == 'minus':
            order_item.quantity -= 1
        elif action == 'remove':
            order_item.quantity = 0

        order.save()
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

    return JsonResponse('item was added', safe=False)


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
