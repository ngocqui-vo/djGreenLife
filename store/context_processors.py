from .models import Category, Order, OrderItem


def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def get_cart_items(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        return {'items_count': order.get_total_items}
    else:
        return {'items_count': 0}
