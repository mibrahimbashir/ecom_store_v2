from django.urls import path
from . import views


urlpatterns = [
    path('cart-summary/', views.cart_summary, name='cart-summary'),
    path('cart-add/<slug:slug>/', views.cart_add, name='cart-add'),
    path(
        'update_quantity/<slug:slug>/',
        views.update_quantity,
        name='update_quantity'
    ),
]