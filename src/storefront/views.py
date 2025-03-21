from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Prefetch
from .forms import CustomerForm
from products.models import Product, ProductImage, Collection


def home(request):
    product_images_prefetch = Prefetch(
        'images', # related_name of ProductImage in Product
        queryset=ProductImage.objects.only(
            'product',
            'image',
            'primary_image'
        ).filter(primary_image=True)
    )

    # Prefetch products with their images for each collection
    all_collections = Collection.objects.only('name', 'image') \
        .prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.only(
                    'name',
                    'price',
                    'discount_percentage'
                ).prefetch_related(product_images_prefetch)
            )
        ).filter(display_on_home=True)

    context = {'all_collections': all_collections}

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
