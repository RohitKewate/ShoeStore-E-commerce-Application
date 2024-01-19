# Generated by Django 4.2 on 2023-08-17 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0015_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="status",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Order Placed", "Order Placed"),
                    ("Order Confirmed", "Order Confirmed"),
                    ("Dispatched", "Dispatched"),
                    ("Shipped", "Shipped"),
                    ("Out for Delivery", "Out for Delivery"),
                    ("Delivered", "Delivered"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
