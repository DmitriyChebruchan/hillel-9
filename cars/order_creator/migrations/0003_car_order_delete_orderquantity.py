# Generated by Django 4.2.6 on 2023-10-26 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("order_creator", "0002_logedinuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="order_creator.order",
            ),
        ),
        migrations.DeleteModel(
            name="OrderQuantity",
        ),
    ]
