# Generated by Django 3.2.5 on 2023-03-20 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20230320_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='is_buying',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='quantity',
        ),
    ]
