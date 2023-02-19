from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.search_products, name='search_products'),
    # path('store/<str:search_str>', views.search_products, name='search_products'),
    path('store/category/<slug:slug>/', views.category_products, name='category_products'),
    path('detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]
