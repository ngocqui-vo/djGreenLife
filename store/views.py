import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Category, Product, Customer, Order, OrderItem


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


def products_price_range(request):
    pass


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


@login_required(login_url='/accounts/login/')
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



