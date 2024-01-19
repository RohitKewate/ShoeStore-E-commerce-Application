# Generated by Django 4.2 on 2023-07-27 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0012_alter_coupon_discount_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="coupon",
        ),
        migrations.AddField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.coupon",
            ),
        ),
    ]