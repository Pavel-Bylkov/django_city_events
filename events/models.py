import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

from django.db.models import Q

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
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return "[{}] {} - {}".format(self.location.city, self.title, self.start_datetime)

    def current_event(self):
        return self.start_datetime >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # Notify users
        if not self.id:
            super(Event, self).save(*args, **kwargs)
            if not self.slug or self.slug == ' ':
                self.slug = 'event-' + str(self.id)
                self.save()
            users = get_users(self)
            if users and len(users) > 0:
                title = f'City Event: Создано событие "{self.title}"'
                msg = (f'Дата публикации {self.pub_datetime.strftime("%d.%m.%Y")}\n---\n' +
                       f'{self.title}:\nОписание: {self.description}\n---\n' +
                       f'Город: {self.location.city} Подробнее по ссылке {self.get_absolute_url()}')
                emails = []
                for user in users:
                    emails.append(user.email)
                    notify = Notifications.objects.create(user=user, title=title, msg=msg)
                    notify.save()
                try:
                    send_mail(title, msg, settings.DEFAULT_FROM_EMAIL,
                      emails, fail_silently=False,)
                except Exception as e:
                    print("error send mail:", e)
        else:
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


def apply_filter(f):
    locations = Location.objects.filter(city=f.city)
    actual_start = f.start_range
    actual_end = f.end_range
    events_list = Event.objects.filter(is_published=True)
    if locations.all():
        events_list = events_list.filter(
            location__in=locations.all())
    if f.topics.all():
        events_list = events_list.filter(
            topics__in=f.topics.all())
    if actual_start and actual_end:
        events_list = events_list.filter(start_datetime__gte=actual_start,
                                         start_datetime__lte=actual_end)
    elif actual_start:
        events_list = events_list.filter(start_datetime__gte=actual_start)
    elif actual_end:
        events_list = events_list.filter(start_datetime__lte=actual_end)
    return events_list.distinct()


def get_users(event):
    """
    Возвращает список users кому отправить уведомление о новом событии.
    """
    filters = EventFilters.objects.filter(
        Q(city=event.location.city) |
        Q(topics__in=event.topics.all()) |
        Q(start_range__gte=event.start_datetime) |
        Q(start_range__lte=event.start_datetime)).distinct()
    check_filters = []
    print(filters)
    for f in filters.all():
        if event in apply_filter(f).all():
        # if apply_filter(f).filter(id=event.id).exists():
            check_filters.append(f)
    users = User.objects.filter(filters__in=check_filters).distinct()
    print(check_filters, users)
    return users
