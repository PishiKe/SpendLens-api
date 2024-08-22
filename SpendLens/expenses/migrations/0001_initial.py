# Generated by Django 5.0.6 on 2024-08-22 03:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.FloatField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
