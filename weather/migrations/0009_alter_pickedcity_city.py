# Generated by Django 3.2 on 2021-06-01 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_pickedcity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickedcity',
            name='city',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='city_picked_related', serialize=False, to='weather.city'),
        ),
    ]
