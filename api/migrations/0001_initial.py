# Generated by Django 3.1.2 on 2023-02-26 23:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)])),
                ('lon', models.FloatField()),
                ('altitude', models.FloatField(validators=[django.core.validators.MaxValueValidator(16383), django.core.validators.MinValueValidator(-16383)])),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
