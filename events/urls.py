from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('detail/<slug:slug>/', views.event, name="event_detail"),
    path("events/", views.index, name='index'),
    path("filter/", views.event_filter, name='event_filter'),
    path("new/", views.new_event, name='new_event'),
    path("my_filters/", views.my_filters, name='my_filters'),
    path("my_notify/", views.my_notify, name='my_notify'),
]
