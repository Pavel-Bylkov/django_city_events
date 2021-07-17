import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.context_processors import auth
from .models import Event, EventFilters, User, Location

from .forms import EventFiltersForm


def index(request):
    """author = User.objects.get(username='tolstoy')
    keyword = "Утро"
    start = datetime.date(2021, 3, 9)
    end = datetime.date(2021, 3, 15)
    posts = Post.objects.filter(
        author=author
        ).filter(
        pub_date__range=(start, end)
        ).filter(
        text__contains=keyword
    )"""
    groups = Group.objects.all()
    posts = Post.objects.all()
    return render(request, "index.html", {"groups": groups, 'posts': posts})


# view-функция для фильтра по slug Location
def location_events(request, slug):
    location = get_object_or_404(Location, slug=slug)
    events = Event.objects.filter(location=location).order_by("-pub_datetime")[:20]
    return render(request, "location.html", {"location": location, "events": events})


@login_required
def new_filter(request):
    if request.method == 'POST':
        bound_form = EventFiltersForm(request.POST)
        if bound_form.is_valid():
            user = auth(request)['user']
            city = bound_form.cleaned_data['city']
            topics = bound_form.cleaned_data['topics']
            start_range = bound_form.cleaned_data['start_range']
            end_range = bound_form.cleaned_data['end_range']
            saved = bound_form.cleaned_data['saved']
            filter = EventFilters.objects.create(user=user, city=city, topics=topics,
                                                 start_range=start_range, end_range=end_range)
            if saved:
                filter.save()
            return redirect('/')
        return render(request, 'events/events.html', {'form': bound_form})

    form = EventFiltersForm()
    return render(request, 'events/events.html', context={'form': form})
