# Generated by Django 3.2.5 on 2021-07-21 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_eventfilters_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='is_cancelled',
        ),
    ]
