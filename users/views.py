from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.shortcuts import render


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "signup.html"


def login(request):
    return render(request, "registration/login.html", {})
