# Generated by Django 5.1.5 on 2025-03-15 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BuySell', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart',
            table='buysell_cart',
        ),
        migrations.AlterModelTable(
            name='items',
            table='buysell_items',
        ),
    ]
