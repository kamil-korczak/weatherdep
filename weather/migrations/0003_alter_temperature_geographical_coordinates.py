# Generated by Django 3.2 on 2021-04-21 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_temperature_current_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='geographical_coordinates',
            field=models.CharField(max_length=200, null=True),
        ),
    ]