# Generated by Django 4.1.3 on 2022-12-01 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='total_price',
        ),
    ]