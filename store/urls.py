from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.all_products, name='all_products'),
    path('store/<slug:slug>/', views.category_products, name='category_products'),
    path('detai/<slug:slug>/', views.product_detail, name='product_detail'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

]