# Generated by Django 3.1.7 on 2021-03-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20210307_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='SastoDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=100)),
                ('original', models.CharField(max_length=100)),
                ('discount', models.CharField(max_length=100)),
            ],
        ),
    ]
