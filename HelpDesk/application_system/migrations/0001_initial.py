# Generated by Django 3.0.3 on 2020-02-13 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
                ('topic', models.CharField(max_length=255)),
                ('text', models.TextField(max_length=500)),
                ('progress', models.CharField(default='', max_length=100)),
                ('is_active', models.CharField(choices=[(1, 'Accept'), (2, 'Reject'), (3, 'Renew'), (4, 'completely rejected')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newcomments', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newcomments', to='application_system.Statement')),
            ],
        ),
    ]