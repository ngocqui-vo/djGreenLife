from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    # path('store/all_product', views.all_products, name='all_products'),
    path('store/', views.search_products, name='search_products'),
    path('store/category/<slug:slug>/', views.category_products, name='category_products'),
    path('detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('update_item/', views.update_item, name='update_item'),
    path('cart/', views.cart, name='cart'),
    path('place_order/', views.place_order, name='place_order'),

]
