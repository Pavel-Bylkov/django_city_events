from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.context_processors import auth
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from .models import Event, EventFilters, User, Location, City, Topics, Notifications
from .forms import EventFiltersForm, EventForm, CityForm, TopicForm, LocationForm


def index(request):
    actual_start = now()
    events_list = Event.objects.filter(is_published=True).filter(
        start_datetime__gte=actual_start).order_by('start_datetime')
    events_past = Event.objects.filter(is_published=True).filter(
        start_datetime__lte=actual_start).order_by('-start_datetime')
    context = {'events_list': events_list, 'events_past': events_past,
               'active': 'events', 'bootstrap': 3}
    return render(request, 'events/index.html', context)


def event_filter(request):
    cities = City.objects.all()
    topics = Topics.objects.all()
    if request.method == 'POST':
        bound_form = EventFiltersForm(request.POST)
        topics_list = topics
        actual_start = None
        actual_end = None
        locations_list = Location.objects.all()
        if bound_form.is_valid():
            if bound_form.cleaned_data['city']:
                city = bound_form.cleaned_data['city']
                locations_list = Location.objects.filter(city=city)
            if bound_form.cleaned_data['topics']:
                topics_list = bound_form.cleaned_data['topics']
            if bound_form.cleaned_data['start_range']:
                actual_start = bound_form.cleaned_data['start_range']
            if bound_form.cleaned_data['end_range']:
                actual_end = bound_form.cleaned_data['end_range']
            if request.user.is_authenticated and bound_form.cleaned_data['saved']:
                filter = EventFilters.objects.create(
                    user=auth(request)['user'],
                    city=bound_form.cleaned_data['city'],
                    start_range=bound_form.cleaned_data['start_range'],
                    end_range=bound_form.cleaned_data['end_range'],
                    saved=bound_form.cleaned_data['saved'])
                filter.topics.set(bound_form.cleaned_data['topics'])
                filter.save()
            events_list = Event.objects.filter(is_published=True).filter(
                location__in=locations_list.all()).filter(
                topics__in=topics_list.all()).distinct()
            if actual_start and actual_end:
                events_list = events_list.filter(start_datetime__gte=actual_start,
                                                 start_datetime__lte=actual_end)
            elif actual_start:
                events_list = events_list.filter(start_datetime__gte=actual_start)
            elif actual_end:
                events_list = events_list.filter(start_datetime__lte=actual_end)
            events_list = events_list.distinct().order_by('start_datetime')
            context = {'events_list': events_list, 'bootstrap': 3, 'search': True}
            return render(request, 'events/index.html', context)
        context = {'active': 'filter', 'cities': cities,
                   'topics': topics, 'form': bound_form, 'bootstrap': 3}
        return render(request, 'events/filter.html', context)

    form = EventFiltersForm()
    context = {'active': 'filter', 'cities': cities,
               'topics': topics, 'form': form, 'bootstrap': 3}
    return render(request, 'events/filter.html', context)


@login_required
def new_event(request):
    form = EventForm()
    newevent = None
    if request.method == 'POST':
        eventform = EventForm(request.POST)
        if eventform.is_valid():
            newevent = eventform.cleaned_data['title']
            new_e = eventform.save()
            send_notify(new_e)
            form = EventForm()
    context = {'form': form, 'newevent': newevent,
               'active': 'new_event'}
    return render(request, 'events/new_event.html', context)


@login_required
def new_city(request):
    cityform = CityForm(prefix='addcity')
    locationform = LocationForm(prefix='addloc')
    topicform = TopicForm(prefix='addtopic')
    city = location = topic = None
    if request.method == 'POST':
        if 'addcity' in request.POST:
            cityform = CityForm(request.POST, prefix='addcity')
            if cityform.is_valid():
                cityform.save()
                city = cityform.cleaned_data['name']
                cityform = CityForm(prefix='addcity')
        if 'addloc' in request.POST:
            locationform = LocationForm(request.POST, prefix='addloc')
            if locationform.is_valid():
                locationform.save()
                location = locationform.cleaned_data['venue']
                locationform = LocationForm(prefix='addloc')
        if 'addtopic' in request.POST:
            topicform = TopicForm(request.POST, prefix='addtopic')
            if topicform.is_valid():
                topicform.save()
                topic = topicform.cleaned_data['name']
                topicform = TopicForm(prefix='addtopic')

    context = {'cityform': cityform, 'locationform': locationform,
               'topicform': topicform, 'city': city,
               'location': location, 'topic': topic,
               'active': 'new_city'}
    return render(request, 'events/new_city_topic_loc.html', context)


def event_detail(request, slug):
    cur_event = get_object_or_404(Event, slug=slug)
    context = {"event": cur_event}

    workshop_ended = True
    if now() < cur_event.end_datetime:
        workshop_ended = False
    context["workshop_ended"] = workshop_ended

    return render(request, 'events/event.html', context)


@login_required
def my_filters(request):
    filters_list = EventFilters.objects.filter(
        user=auth(request)['user']).order_by('-save_datetime')
    context = {'filters_list': filters_list,
               'active': 'my_filters', 'bootstrap': 3}
    return render(request, 'events/my_filters.html', context)


@login_required
def my_notify(request):
    notify_list = Notifications.objects.filter(
        user=auth(request)['user']).order_by('-create_datetime')
    context = {'notify_list': notify_list,
               'active': 'my_notify', 'bootstrap': 3}
    return render(request, 'events/my_notify.html', context)


def apply_f(f):
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
        events_list = events_list.filter(start_datetime__range=(actual_start,
                                         actual_end))
    elif actual_start:
        events_list = events_list.filter(start_datetime__gte=actual_start)
    elif actual_end:
        events_list = events_list.filter(start_datetime__lte=actual_end)
    return events_list.distinct()


@login_required
def apply_filter(request, id):
    f = EventFilters.objects.get(id=id)
    events_list = apply_f(f).order_by('start_datetime')
    context = {'events_list': events_list, 'bootstrap': 3, 'search': True}
    return render(request, 'events/index.html', context)


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
    for f in filters.all():
        if event in apply_f(f):
            check_filters.append(f)
    users = User.objects.filter(filters__in=check_filters).distinct()
    return users


def send_notify(event):
    users = get_users(event)
    if users and len(users) > 0:
        title = f'City Event: Создано событие "{event.title}"'
        msg = (f'Дата публикации {event.pub_datetime.strftime("%d.%m.%Y")}\n---\n' +
               f'{event.title}:\nОписание: {event.description}\n---\n' +
               f'Город: {event.location.city} '
               f'Подробнее по ссылке <a href="http://127.0.0.1:8000{event.get_absolute_url()}">Подробнее</a>')
        emails = []
        for user in users:
            emails.append(user.email)
            notify = Notifications.objects.create(user=user, title=title, msg=msg)
            notify.save()
        try:
            send_mail(title, msg, settings.DEFAULT_FROM_EMAIL,
                      emails, fail_silently=False, )
        except Exception as e:
            print("error send mail:", e)
