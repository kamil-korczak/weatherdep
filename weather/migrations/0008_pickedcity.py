# Generated by Django 3.2 on 2021-06-01 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0007_auto_20210531_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickedCity',
            fields=[
                ('city', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='weather.city')),
            ],
        ),
    ]
