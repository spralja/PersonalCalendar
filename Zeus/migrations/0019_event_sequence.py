# Generated by Django 4.0.1 on 2022-01-15 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Zeus', '0018_event_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sequence',
            field=models.IntegerField(null=True),
        ),
    ]