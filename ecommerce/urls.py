from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<str:order_number>/', views.order_success, name='order_success'),
    path('order/track/', views.order_tracking, name='order_tracking'),
    path('order/invoice/<str:order_number>/', views.order_invoice, name='order_invoice'),
    path('dashboard/orders/', views.order_dashboard, name='order_dashboard'),
    path('dashboard/orders/<int:order_id>/status/', views.order_update_status, name='order_update_status'),
]
