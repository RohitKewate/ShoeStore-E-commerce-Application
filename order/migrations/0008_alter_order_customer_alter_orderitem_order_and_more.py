# Generated by Django 4.2 on 2023-07-25 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_address_district_profile_phone_number"),
        ("order", "0007_alter_orderitem_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="account.profile",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]