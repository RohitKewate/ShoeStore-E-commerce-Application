# Generated by Django 4.2 on 2023-07-20 12:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now=True)),
                ("updated", models.DateTimeField(auto_now_add=True)),
                ("category_name", models.CharField(max_length=100)),
                ("slug", models.SlugField(blank=True, null=True, unique=True)),
                ("category_image", models.ImageField(upload_to="categories")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now=True)),
                ("updated", models.DateTimeField(auto_now_add=True)),
                ("product_name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("price", models.IntegerField()),
                ("product_description", models.TextField(max_length=500)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="product.category",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now=True)),
                ("updated", models.DateTimeField(auto_now_add=True)),
                ("image", models.ImageField(upload_to="product")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_images",
                        to="product.product",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
