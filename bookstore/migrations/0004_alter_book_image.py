# Generated by Django 5.0 on 2023-12-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(upload_to='book_images/'),
        ),
    ]
