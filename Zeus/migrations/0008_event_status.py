# Generated by Django 4.0.1 on 2022-01-16 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zeus', '0007_event_resources'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.TextField(null=True),
        ),
    ]
