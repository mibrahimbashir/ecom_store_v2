from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    # non-nullable and non-editable field, value is set when saving the model
    slug = models.SlugField(
        max_length=255, unique=True, blank=True, editable=False
    )
    description = models.TextField(help_text='Markdown supported')
    notes = models.TextField(
        blank=True, null=True, help_text='Markdown supported'
    )
    performance = models.TextField(
        blank=True, null=True, help_text='Markdown supported'
    )
    additional_info = models.TextField(
        blank=True, null=True, help_text='Markdown supported'
    )
    collections = models.ManyToManyField(
        'Collection', blank=True, related_name='products'
    )
    size = models.CharField(max_length=32)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0.0)]
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    discount_percentage = models.PositiveSmallIntegerField(
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    mark_as_deleted = models.BooleanField(
        blank=True,
        default=False,
        verbose_name='Mark product as deleted (soft delete)',
        help_text='Marking this field wll not actually delete the product, \
              since this is a sentinel value.'
    )
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

    @property
    def on_sale(self):
        return True if self.discount_percentage else False

    @property
    def discounted_price(self):
        # return discounted price if product is on sale
        if self.on_sale:
            return int(
                self.price - (self.price * self.discount_percentage / 100)
            )

    @property
    def total_savings(self):
        # returns total savings if product is on sale
        if self.on_sale:
            # cast price field from decimal to float dtype
            return int(float(self.price) - self.discounted_price)

    @property
    def is_available(self):
        return True if self.quantity else False

    def save(self, *args, **kwargs):
        # product is marked as deleted, set deleted_at field to current \
        #  time and quantity to 0
        if self.mark_as_deleted:
            self.deleted_at = timezone.now()
            self.quantity = 0

        # product was previously marked as deleted, but now it's restored \
        #  so, set the deleted_at field to None
        if not self.mark_as_deleted and self.deleted_at:
            self.deleted_at = None

        # set value of slug field
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        default='product_images/default-product-image.png',
        blank=True,
        null=True,
        related_name='images'
    )
    image = models.ImageField(upload_to='product_images/')
    primary_image = models.BooleanField(blank=True, default=False)


class Collection(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text='Define a descriptive collection name. This name will be \
            used as heading when displaying products.'
    )
    image = models.ImageField(
        upload_to='collection_images/', blank=True, null=True,
    )
    display_on_home = models.BooleanField(
        verbose_name='Display products in this collection on home page?',
        default=False,
    )

    def __str__(self):
        return self.name
