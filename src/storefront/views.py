from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomerForm


def home(request):
    context = {}

    return render(request, 'storefront/home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # render form with errors
            return render(request, 'registration/register.html', {'form': form})

    return render(request, 'registration/register.html', {'form': form})
