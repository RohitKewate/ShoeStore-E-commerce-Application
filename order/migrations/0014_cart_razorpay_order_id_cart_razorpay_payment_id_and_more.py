# Generated by Django 4.2 on 2023-07-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0013_remove_cart_coupon_order_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
