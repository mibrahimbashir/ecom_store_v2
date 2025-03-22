from django.urls import path
from . import views


urlpatterns = [
    path('p/<slug:slug>/', views.product_page, name="product_page")
]