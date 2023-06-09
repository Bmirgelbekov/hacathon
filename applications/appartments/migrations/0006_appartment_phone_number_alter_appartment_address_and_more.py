# Generated by Django 4.2 on 2023-04-06 11:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appartments', '0005_alter_appartment_image_alter_comment_sub_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appartment',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, validators=[django.core.validators.RegexValidator('^\\d+$', 'Введите только цифры')]),
        ),
        migrations.AlterField(
            model_name='appartment',
            name='address',
            field=models.CharField(default='не указано', max_length=200),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
