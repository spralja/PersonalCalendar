# Generated by Django 4.0.1 on 2022-01-17 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zeus', '0010_remove_calendar_calscale_remove_calendar_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='_class',
        ),
        migrations.RemoveField(
            model_name='event',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='event',
            name='created',
        ),
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='geo',
        ),
        migrations.RemoveField(
            model_name='event',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.RemoveField(
            model_name='event',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='event',
            name='related_to',
        ),
        migrations.RemoveField(
            model_name='event',
            name='resources',
        ),
        migrations.RemoveField(
            model_name='event',
            name='sequence',
        ),
        migrations.RemoveField(
            model_name='event',
            name='status',
        ),
        migrations.RemoveField(
            model_name='event',
            name='uri',
        ),
    ]
