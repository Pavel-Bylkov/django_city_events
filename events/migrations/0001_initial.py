# Generated by Django 3.2.5 on 2021-07-18 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, null=True, verbose_name='Заголовок темы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=250, verbose_name='Место проведения')),
                ('address1', models.CharField(blank=True, max_length=250)),
                ('address2', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(help_text='Например: crocuscityhall-moscow', null=True)),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='events.city')),
            ],
        ),
        migrations.CreateModel(
            name='EventFilters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_range', models.DateTimeField(blank=True)),
                ('end_range', models.DateTimeField(blank=True)),
                ('saved', models.BooleanField(default=False)),
                ('city', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='events.city')),
                ('topics', models.ManyToManyField(blank=True, to='events.Topics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название события')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('pub_datetime', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('event_url', models.URLField()),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('is_published', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.location', verbose_name='Место проведения')),
                ('topics', models.ManyToManyField(related_name='events', to='events.Topics', verbose_name='Темы')),
            ],
            options={
                'ordering': ['-start_datetime'],
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='events.country'),
        ),
    ]
