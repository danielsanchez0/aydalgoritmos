# Generated by Django 4.0.3 on 2022-03-19 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('algoritmosApp', '0003_graphs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphs',
            name='aristas',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='graphs',
            name='nodos',
            field=models.TextField(default='{}'),
        ),
    ]
