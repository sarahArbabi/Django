# Generated by Django 4.1.3 on 2022-12-06 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='peoduct_image',
            new_name='product_image',
        ),
    ]