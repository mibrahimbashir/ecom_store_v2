from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('search-modal/', views.search_modal, name='search-modal'),
    path('menu-content/', views.menu_content, name='menu-content'),
    path('search-results/', views.search_results, name='search-results'),
    path(
        'get-header-content/',
        views.get_header_content,
        name='get-header-content'
    ),
]