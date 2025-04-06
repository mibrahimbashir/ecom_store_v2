from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.user_profile, name='profile'),
    path('user_info_form/', views.user_info_form, name='user_info_form'),
]