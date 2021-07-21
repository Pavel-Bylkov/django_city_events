import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=250, null=True)
    country = models.ForeignKey(Country, null=True, blank=False,
                                on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Location(models.Model):
    venue = models.CharField(max_length=250, verbose_name='Место проведения')
    address1 = models.CharField(blank=True, max_length=250)
    address2 = models.CharField(blank=True, max_length=250)
    city = models.ForeignKey(City, null=True, blank=False, on_delete=models.CASCADE,
                             related_name='locations')
    slug = models.SlugField(null=True, help_text="Например: crocuscityhall-moscow")

    def __str__(self):
        return "{}, {}".format(self.venue, self.city)

    def save(self, *args, **kwargs):
        super(Location, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.venue}-{self.city}")
            self.save()
        if not self.slug:
            self.slug = f"loc-{self.id}"
            self.save()


class Topics(models.Model):
    name = models.CharField(null=True, max_length=300, verbose_name='Заголовок темы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class EventFilters(models.Model):
    user = models.ForeignKey(User, blank=False, related_name='filters', on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topics, blank=True)
    start_range = models.DateTimeField(auto_now=False, auto_now_add=False,
                                          null=True, blank=True)
    end_range = models.DateTimeField(auto_now=False, auto_now_add=False,
                                        null=True, blank=True)
    saved = models.BooleanField(default=False)
    save_datetime = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('apply_filter', kwargs={'id': self.id})


class Event(models.Model):
    title = models.CharField(max_length=250, blank=False, verbose_name='Название события')
    description = models.TextField(blank=True, null=False, verbose_name='Описание')
    topics = models.ManyToManyField(Topics, blank=False, related_name='events',
                                    verbose_name='Темы')
    location = models.ForeignKey(Location, blank=False, related_name='events',
                                 on_delete=models.CASCADE,
                                 verbose_name='Место проведения')
    pub_datetime = models.DateTimeField(auto_now=True)
    start_datetime = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    end_datetime = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
    slug = models.SlugField(blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return "[{}] {} - {}".format(self.location.city, self.title, self.start_datetime)

    def current_event(self):
        return self.start_datetime >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == ' ':
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)
        if not self.slug or self.slug == ' ':
            self.slug = 'event-' + str(self.id)
            self.save()

    class Meta:
        ordering = ["-start_datetime"]


class Notifications(models.Model):
    user = models.ForeignKey(User, blank=False, related_name='notifies', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, blank=False, verbose_name='Заголовок')
    msg = models.TextField(blank=True, null=False, verbose_name='Сообщение')
    is_read = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[{}] {} - {}".format(self.create_datetime, self.user.username, self.msg)

    class Meta:
        ordering = ["-create_datetime"]



