# Generated by Django 5.1.7 on 2025-03-21 01:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, help_text='Define a descriptive collection name. This name will be             used as heading when displaying products.', max_length=64, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='collection_images/')),
                ('display_on_home', models.BooleanField(default=False, verbose_name='Display products in this collection on home page?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, unique=True)),
                ('description', models.TextField(help_text='Markdown supported')),
                ('notes', models.TextField(blank=True, help_text='Markdown supported', null=True)),
                ('performance', models.TextField(blank=True, help_text='Markdown supported', null=True)),
                ('additional_info', models.TextField(blank=True, help_text='Markdown supported', null=True)),
                ('size', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('discount_percentage', models.PositiveSmallIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('mark_as_deleted', models.BooleanField(blank=True, default=False, help_text='Marking this field wll not actually delete the product,               since this is a sentinel value.', verbose_name='Mark product as deleted (soft delete)')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('collections', models.ManyToManyField(blank=True, related_name='products', to='products.collection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='product_images/')),
                ('primary_image', models.BooleanField(blank=True, default=False)),
                ('product', models.ForeignKey(blank=True, default='product_images/default-product-image.png', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
