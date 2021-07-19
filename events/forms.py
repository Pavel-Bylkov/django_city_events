from django import forms
from django.contrib.admin import widgets
from .models import EventFilters, Event, Topics, City

from datetimewidget.widgets import DateTimeWidget

class EventFiltersForm(forms.ModelForm):
    class Meta:
        model = EventFilters
        fields = ["city", "topics", "start_range", "end_range", "saved"]
        labels = {
            "city": 'Выбрать город',
            "topics": "выбрать темы",
            "start_range": 'События после даты-времени',
            "end_range": 'События до даты-времени',
            "saved": "Сохранить (оповещать о новых)"
        }
        widgets = {
            "city": forms.Select(),
            "topics": forms.SelectMultiple(),
            "start_range": DateTimeWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=3),
            "end_range": DateTimeWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=3),
            "saved": forms.CheckboxInput()
        }


# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ["city", "topics", "start_range", "end_range", "saved"]
#         labels = {
#             "city": 'Выбрать город',
#             "topics": "выбрать темы",
#             "start_range": 'События после даты-времени',
#             "end_range": 'События до даты-времени',
#             "saved": "Сохранить (оповещать о новых)"
#         }
#         widgets = {
#             "city": forms.Select(),
#             "topics": forms.SelectMultiple(),
#             "start_range": forms.DateTimeInput(),
#             "end_range": forms.DateTimeInput(),
#             "saved": forms.CheckboxInput()
#         }
