# Generated by Django 3.0.2 on 2020-01-30 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200130_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='quantity_by_product',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
