# Generated by Django 4.0.1 on 2022-01-14 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Zeus', '0006_alter_event_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='calendar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Zeus.calendar'),
        ),
    ]
