# Generated by Django 4.0.3 on 2022-03-18 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algoritmosApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='departamentName',
            field=models.CharField(max_length=600),
        ),
    ]
