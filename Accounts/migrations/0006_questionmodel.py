# Generated by Django 4.1.4 on 2022-12-16 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('que', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
