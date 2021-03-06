from django import forms
from .models import EventFilters, Event, Topics, City, Location

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


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["name", "country"]
        labels = {
            'name': 'Название',
            'country': 'Выберите страну'
        }
        widgets = {
            'name': forms.TextInput(),
            'country': forms.Select()
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ["name", "description"]
        labels = {
            'name': 'Название',
            'description': 'Описание темы'
        }
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea()
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["venue", 'address1', 'address2', 'city', 'slug']
        labels = {
            'venue': 'Название Места проведения',
            'address1': 'Поле для адреса',
            'address2': 'Поле для адреса',
            'city': 'Выберите город',
            'slug': 'Слаг (английскими буквами и цифрами без пробелов)'
        }
        widgets = {
            'venue': forms.TextInput(),
            'address1': forms.TextInput(),
            'address2': forms.TextInput(),
            'city': forms.Select(),
            'slug': forms.TextInput()
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", 'description', 'topics', 'start_datetime',
                  'end_datetime', 'location', 'is_published']
        labels = {
            'title': 'Название события',
            'description': 'Описание',
            'location': 'Место проведения',
            'topics': 'Обсуждаемые темы',
            'start_datetime': 'Дата и время начала (dd/mm/yyyy hh:ii или dd.mm.yyyy hh:ii)',
            'end_datetime': 'Дата и время окончания (dd/mm/yyyy hh:ii или dd.mm.yyyy hh:ii)',
            'is_published': 'Опубликовать'
        }
        dateTimeOptions = {
            'format': 'dd/mm/yyyy hh:ii',
            'autoclose': True,
        }
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'location': forms.Select(),
            'topics': forms.SelectMultiple(attrs={'required': True}),
            'start_datetime': DateTimeWidget(attrs={'id': "id_start_datetime", 'class': "form-control",
                                                    'required': True},
                                          options=dateTimeOptions, bootstrap_version=3),
            'end_datetime': DateTimeWidget(attrs={'id': "id_end_datetime", 'class': "form-control",
                                                    'required': True},
                                          options=dateTimeOptions, bootstrap_version=3),
            'is_published': forms.CheckboxInput()
        }
