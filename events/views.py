import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.context_processors import auth
from django.utils.timezone import now

from .models import Event, EventFilters, User, Location, City, Topics, Notifications
from .forms import EventFiltersForm, EventForm, CityForm, TopicForm, LocationForm


def index(request):
    actual_start = now() - datetime.timedelta(days=1)
    actual_end = now() + datetime.timedelta(days=30)
    events_list = Event.objects.filter(is_published=True).filter(
        start_datetime__range=(actual_start, actual_end)).order_by('start_datetime')
    events_past = Event.objects.filter(is_published=True).filter(
        start_datetime__lte=actual_start).order_by('-start_datetime')
    context = {'events_list': events_list, 'events_past': events_past,
               'active': 'events', 'bootstrap': 3}
    return render(request, 'events/index.html', context)


def event_filter(request):
    actual_start = now() - datetime.timedelta(days=1)
    actual_end = now() + datetime.timedelta(days=30)
    locations_list = Location.objects.all()
    cities = City.objects.all()
    topics = Topics.objects.all()
    if request.method == 'POST':
        bound_form = EventFiltersForm(request.POST)
        topics_list = topics
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
                location__in=locations_list).filter(
                topics__in=topics_list).distinct().filter(
                start_datetime__range=(actual_start, actual_end)).order_by('start_datetime')
            context = {'events_list': events_list, 'active': 'events', 'bootstrap': 3}
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
    cityform = CityForm(prefix='addcity')
    locationform = LocationForm(prefix='addloc')
    topicform = TopicForm(prefix='addtopic')
    eventform = EventForm(prefix='newevent')
    city = location = topic = newevent = None
    if request.method == 'POST':
        if 'addcity' in request.POST:
            cityform = CityForm(request.POST, prefix='addcity')
            if cityform.is_valid():
                cityform.save()
                city = cityform.cleaned_data['name']
        if 'addloc' in request.POST:
            locationform = LocationForm(request.POST, prefix='addloc')
            if locationform.is_valid():
                locationform.save()
                location = locationform.cleaned_data['venue']
        if 'addtopic' in request.POST:
            topicform = TopicForm(request.POST, prefix='addtopic')
            if topicform.is_valid():
                topicform.save()
                topic = topicform.cleaned_data['name']
        if 'newevent' in request.POST:
            eventform = EventForm(request.POST, prefix='newevent')
            if eventform.is_valid():
                eventform.save()
                newevent = eventform.cleaned_data['title']
    context = {'cityform': cityform, 'locationform': locationform,
               'topicform': topicform, 'eventform': eventform, 'city': city,
               'location': location, 'topic': topic, 'newevent': newevent,
               'active': 'new_event'}
    return render(request, 'events/new_event.html', context)


def event(request, slug):
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
