# Generated by Django 4.1.4 on 2022-12-09 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0005_productmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='price',
            new_name='all_price',
        ),
    ]
