# Generated by Django 4.2 on 2023-07-26 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_alter_product_slug"),
        ("order", "0008_alter_order_customer_alter_orderitem_order_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="orderitem",
            unique_together={("order", "product", "size_varient", "color_varient")},
        ),
    ]
