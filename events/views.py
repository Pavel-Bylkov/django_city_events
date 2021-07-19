import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.context_processors import auth
from django.utils.timezone import now

from .models import Event, EventFilters, User, Location, City, Topics
from .forms import EventFiltersForm


def index(request):
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
                    topics=bound_form.cleaned_data['topics'],
                    start_range=bound_form.cleaned_data['start_range'],
                    end_range=bound_form.cleaned_data['end_range'],
                    saved=bound_form.cleaned_data['saved'])
                filter.save()
        events_list = Event.objects.filter(is_published=True).filter(
            location__in=locations_list).filter(
            topics__in=topics_list).distinct().filter(
            start_datetime__range=(actual_start, actual_end)).order_by('start_datetime')
        context = {'events_list': events_list, 'active': 'events', 'cities': cities,
                   'topics': topics, 'form': bound_form, 'bootstrap': 3}
        return render(request, 'events/index.html', context)

    form = EventFiltersForm()
    events_list = Event.objects.filter(is_published=True).filter(
        start_datetime__range=(actual_start, actual_end)).order_by('start_datetime')
    context = {'events_list': events_list, 'active': 'events', 'cities': cities,
               'topics': topics, 'form': form, 'bootstrap': 3}
    return render(request, 'events/index.html', context)


# view-функция для фильтра по slug Location
def location_events(request, slug):
    location = get_object_or_404(Location, slug=slug)
    events = Event.objects.filter(location=location).order_by("start_datetime")[:20]
    return render(request, "location.html", {"location": location, "events": events})


# @login_required
# def new_event(request):
#     if request.method == 'POST':
#         bound_form = EventFiltersForm(request.POST)
#         if bound_form.is_valid():
#             user = auth(request)['user']
#             city = bound_form.cleaned_data['city']
#             topics = bound_form.cleaned_data['topics']
#             start_range = bound_form.cleaned_data['start_range']
#             end_range = bound_form.cleaned_data['end_range']
#             saved = bound_form.cleaned_data['saved']
#             filter = EventFilters.objects.create(user=user, city=city, topics=topics,
#                                                  start_range=start_range, end_range=end_range)
#             if saved:
#                 filter.save()
#             return redirect('/')
#         return render(request, 'events/events.html', {'form': bound_form})
#
#     form = EventFiltersForm()
#     return render(request, 'events/events.html', context={'form': form})

def event(request, slug):
    cur_event = get_object_or_404(Event, slug=slug)
    print(cur_event)
    context = {"event": cur_event}

    workshop_ended = True
    if now() < cur_event.end_datetime:
        workshop_ended = False
    context["workshop_ended"] = workshop_ended

    return render(request, 'events/event.html', context)

