# Generated by Django 4.1.3 on 2022-12-03 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_product_category_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('None', 'none'), ('Color', 'color'), ('Size', 'size')], max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unit_price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField()),
                ('color_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.color')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('size_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.size')),
            ],
        ),
    ]