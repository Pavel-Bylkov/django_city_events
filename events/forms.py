from django import forms
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
        dateTimeOptions = {
            'format': 'dd/mm/yyyy hh:ii',
            'autoclose': True,
        }
        widgets = {
            "city": forms.Select(),
            "topics": forms.SelectMultiple(),
            "start_range": DateTimeWidget(attrs={'id': "id_start_range"},
                                          options=dateTimeOptions, bootstrap_version=3),
            "end_range": DateTimeWidget(attrs={'id': "id_start_range"},
                                          options=dateTimeOptions, bootstrap_version=3),
            "saved": forms.CheckboxInput()
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'title': 'Название события',
            'description': 'Описание',
            'topics': 'Обсуждаемые темы',
            'start_datetime': 'Дата и время начала',
            'end_datetime': 'Дата и время окончания',
            'location': 'Место проведения',
            'slug': 'Слаг (английскими буквами и цифрами без пробелов)',
            'is_published': 'Опубликовать',
            'is_cancelled': 'Отменить'
        }
        dateTimeOptions = {
            'format': 'dd/mm/yyyy hh:ii',
            'autoclose': True,
        }
        widgets = {
            'title': forms.CharField(),
            'description': forms.Textarea(),
            'topics': forms.SelectMultiple(),
            'start_datetime': DateTimeWidget(attrs={'id': "id_start_datetime"},
                                          options=dateTimeOptions, bootstrap_version=3),
            'end_datetime': DateTimeWidget(attrs={'id': "id_end_datetime"},
                                          options=dateTimeOptions, bootstrap_version=3),
            'location': forms.Select(),
            'slug': forms.SlugField(),
            'is_published': forms.CheckboxInput(),
            'is_cancelled': forms.CheckboxInput()
        }
