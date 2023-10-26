# Generated by Django 4.2.6 on 2023-10-26 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("order_creator", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogedInUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="order_creator.client",
                    ),
                ),
            ],
        ),
    ]