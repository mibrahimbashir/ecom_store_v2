from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db.models import Prefetch
from django.views.decorators.http import require_http_methods
from .forms import CustomerForm
from products.models import Product, ProductImage, Collection


@require_http_methods(['GET'])
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
                    'discount_percentage',
                    'slug'
                ).prefetch_related(product_images_prefetch)
            )
        ).filter(display_on_home=True)

    context = {'all_collections': all_collections}

    return render(request, 'storefront/home.html', context)


@require_http_methods(['GET'])
def get_header_content(request):
    # not an AJAX request
    if not request.headers.get('HX-Request'):
        return HttpResponseForbidden()

    all_collections = Collection.objects.only('name')

    context = {'all_collections': all_collections}
    
    return render(request, 'storefront/header.html', context)


@require_http_methods(['GET'])
def search_modal(request):
    # not an AJAX request
    if not request.headers.get('HX-Request'):
        return HttpResponseForbidden()

    return render(request, 'storefront/search_modal.html')


@require_http_methods(['POST'])
def search_results(request):
    # not an AJAX request
    if not request.headers.get('HX-Request'):
        return HttpResponseForbidden()

    # get value of input element;
    searched_keyword = request.POST.get('search', '')

    if not searched_keyword:
        return render(request, 'storefront/search_results.html')

    product_images_prefetch = Prefetch(
        'images', # related_name of ProductImage in Product
        queryset=ProductImage.objects.only(
            'product',
            'image',
            'primary_image'
        ).filter(primary_image=True)
    )

    products = Product.objects.only('name', 'price') \
        .prefetch_related(product_images_prefetch) \
            .filter(name__icontains=searched_keyword, mark_as_deleted=False)

    context = {'products': products}

    return render(request, 'storefront/search_results.html', context)


def menu_content(request):
    # not an AJAX request
    if not request.headers.get('HX-Request'):
        return HttpResponseForbidden()

    all_collections = Collection.objects.only('name')

    context = {'all_collections': all_collections}
    
    return render(request, 'storefront/hamburger_menu.html', context)

@require_http_methods(['GET', 'POST'])
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
