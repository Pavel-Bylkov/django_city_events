from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("new/", views.new_event, name='new_event'),
    path("loc/<slug:slug>/", views.location_events, name='location_events'),
]
