# Generated by Django 2.1.7 on 2019-09-30 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='product/%Y/%m/%d'),
        ),
    ]
