# Generated by Django 3.2.5 on 2023-03-16 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_inventory_is_buying'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='is_in_inventory',
            field=models.BooleanField(default=False),
        ),
    ]
