from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created', )

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.customer.first_name} {self.customer.last_name}'

    @property
    def get_total_items(self):
        order_items = self.order_items.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_total_prices(self):
        order_items = self.order_items.all()
        total = sum([item.get_price for item in order_items])
        return total

    @property
    def get_tax(self):
        return self.get_total_prices * 3 / 100

    @property
    def get_prices_with_tax(self):
        return self.get_total_prices + self.get_tax


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='order_items')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    @property
    def get_price(self):
        return self.product.price * self.quantity


class Delivery(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street


PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=256)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    payer_id = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_id
