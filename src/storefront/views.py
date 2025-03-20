from django.shortcuts import render, redirect


def home(request):
    context = {}

    return render(request, 'storefront/home.html', context)
