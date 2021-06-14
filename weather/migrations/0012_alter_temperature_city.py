# Generated by Django 3.2 on 2021-06-03 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0011_auto_20210603_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temperature_related', to='weather.city'),
        ),
    ]