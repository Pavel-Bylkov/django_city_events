from django import forms
from .models import EventFilters


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
            "start_range": forms.DateTimeInput(),
            "end_range": forms.DateTimeInput(),
            "saved": forms.CheckboxInput()
        }
