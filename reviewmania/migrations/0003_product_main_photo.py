# Generated by Django 3.2.13 on 2022-06-21 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewmania', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_photo',
            field=models.ImageField(blank=True, upload_to='products'),
        ),
    ]