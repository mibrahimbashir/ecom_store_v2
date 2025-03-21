from django.contrib import admin
from .models import Product, ProductImage, Collection


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    model = Product

    def on_sale(self, obj):
        return obj.on_sale

    empty_value_display = '-Empty-'    
    readonly_fields = [
        'discounted_price', 'on_sale', 'deleted_at', 'slug', 'total_savings'
    ]
    list_display = ['name', 'price', 'quantity', 'on_sale', 'updated_at']
    list_filter = ['collections']
    search_fields = ['name']
    filter_horizontal = ['collections']
    inlines = [ProductImageInline]

    fieldsets = [
        ('Basic Info', {'fields': ['name', 'size', 'description']}),
        (
            'Price Info',
            {
                'fields': [
                    'price',
                    'quantity',
                    'discount_percentage',
                    ('on_sale', 'discounted_price', 'total_savings'),
                ]
            },
        ),
        ('Collections', {'classes': ['collapse'], 'fields': ['collections']}),
        (
            'Additional Info',
            {
                'classes': ['collapse'],
                'fields': ['notes', 'performance', 'additional_info']
            },
        ),
        (
            'Danger',
            {
                'classes': ['collapse'],
                'fields': ['mark_as_deleted', 'deleted_at']
            },
        ),
    ]


admin.site.register(Collection)
admin.site.register(Product, ProductAdmin)