# Generated by Django 2.2.6 on 2019-10-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20191018_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='abc', null=True),
        ),
    ]
