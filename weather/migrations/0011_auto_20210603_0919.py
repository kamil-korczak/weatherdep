# Generated by Django 3.2 on 2021-06-03 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0010_auto_20210603_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickedcity',
            name='city',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='picked_city_related', serialize=False, to='weather.city'),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_related_to_temperature', to='weather.city'),
        ),
    ]