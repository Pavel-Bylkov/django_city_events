from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path('detail/<slug:slug>/', views.event_detail, name="event_detail"),
    path("events/", views.index, name='index'),
    path("filter/", views.event_filter, name='event_filter'),
    path('apply_filter/<int:id>/', views.apply_filter, name="apply_filter"),
    path("new/", views.new_event, name='new_event'),
    path("new_city/", views.new_city, name='new_city'),
    path("my_filters/", views.my_filters, name='my_filters'),
    path("my_notify/", views.my_notify, name='my_notify'),
]
