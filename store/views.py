from django.shortcuts import render
from .models import Category, Product


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
    return render(request, 'store/')
