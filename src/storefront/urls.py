from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path(
        'get-header-content/',
        views.get_header_content,
        name='get-header-content'
    ),
]