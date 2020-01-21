# Generated by Django 3.0.2 on 2020-01-17 21:46

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cash', models.PositiveIntegerField(default=10000)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('product_description', models.TextField(max_length=150)),
                ('price', models.PositiveIntegerField()),
                ('quantity_product', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_by_product', models.PositiveIntegerField()),
                ('purchase_time', models.DateTimeField(auto_now_add=True)),
                ('info_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
                ('info_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Person')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('return_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Purchase')),
            ],
        ),
    ]
