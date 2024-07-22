from django.shortcuts import render
from django.views import generic
from .forms import CustumUserCreationForm
from django.urls import reverse_lazy


class SignUpView(generic.CreateView):
    form_class = CustumUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    