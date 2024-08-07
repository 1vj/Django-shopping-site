# Generated by Django 5.0.1 on 2024-03-12 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50)),
                ('item_name', models.CharField(max_length=50)),
                ('desc', models.CharField(blank=True, max_length=200)),
                ('discounted_price', models.IntegerField()),
                ('actual_price', models.IntegerField()),
                ('available_number', models.IntegerField()),
                ('image', models.ImageField(default='images/loading.png', upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('is_admin', models.BooleanField(default=False)),
                ('lastLogin', models.DateTimeField(null=True)),
                ('cart_value', models.IntegerField(default=0)),
                ('cart_item', models.JSONField(blank=True, null=True)),
                ('order', models.JSONField(blank=True, null=True)),
                ('order_value', models.IntegerField(default=0)),
                ('auth_token', models.CharField(default=None, max_length=200, null=True)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_discounted_price', models.IntegerField(default=0)),
                ('product', models.ManyToManyField(to='shopping_app.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.user')),
            ],
        ),
    ]