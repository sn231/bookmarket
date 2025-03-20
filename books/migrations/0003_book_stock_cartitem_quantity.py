# Generated by Django 5.1.5 on 2025-03-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_category_book_favorites_book_views_book_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='stock',
            field=models.PositiveIntegerField(default=1, verbose_name='库存数量'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='数量'),
        ),
    ]
