# Importing models
from django.contrib.auth.models import User

# Importing library stuff
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from annoying.decorators import render_to
import random
from django.contrib.auth.views import login, logout
from django.contrib.auth import login as userlogin
from django.contrib.auth import authenticate

# Importing our own stuff
from csc450.cars.models import *
from csc450.cars.forms import UserRegisterForm, CarForm

@render_to('index.html')
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    return {}

@render_to('user_register.html')
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            userlogin(request, new_user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = UserRegisterForm()
    return {'form': form}

def user_login(request):
    return login(request, template_name='user_login.html')

def user_logoff(request):
    return logout(request, template_name='user_logoff.html', next_page=reverse('index'))

@render_to('dashboard.html')
def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    cars = request.user.vehicle_set.all()
    return {'cars': cars}

@render_to('add_car.html')
def add_car(request):
    if request.method == 'POST':
        form = CarForm(data=request.POST)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.owner = request.user
            new_car.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = CarForm()
    return {'form': form}

@render_to('car_detail.html')
def car_detail(request, id):
    car = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        form = CarForm(data=request.POST, instance=car)
        if form.is_valid():
            car = form.save()
            return HttpResponseRedirect(reverse('car_detail', kwargs={'id': id}))
    else:
        form = CarForm(instance=car)
    return {'car': car, 'form': form}
