# Generated by Django 5.0.1 on 2024-03-18 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ManyToManyField(to='shopping_app.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.user')),
            ],
        ),
    ]
