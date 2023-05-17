from django.shortcuts import render
from django.views.generic import CreateView
from .models import User
from .forms import UserCreationForms


class Register(CreateView):
    model = User
    form_class = UserCreationForms
    template_name = 'register.html'
    success_url = 'success'


def success_view(request):
    return render(request, 'success.html')
