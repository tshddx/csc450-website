# Importing models
from django.contrib.auth.models import User

# Importing library stuff
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from annoying.decorators import render_to
import random
from django.contrib.auth.views import login, logout
from django.contrib.auth import login as userlogin
from django.contrib.auth import authenticate

# Importing our own stuff
from cars.models import *
from cars.forms import *

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
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
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
    vehicles = request.user.vehicle_set.all()
    print vehicles
    return {'vehicles': vehicles}

@render_to('add_car.html')
def add_car(request):
    if request.method == 'POST':
        form = VehicleForm(data=request.POST)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.owner = request.user
            new_car.save()
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = VehicleForm()
    return {'form': form}

class VehicleCreateView(CreateView):
    context_object_name = "vehicle"
    model = Vehicle

# TODO: make sure users can only see their own vehicles
class VehicleUpdateView(UpdateView):
    context_object_name = "vehicle"
    model = Vehicle
    form_class = VehicleForm
    template_name = "vehicle_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super(PublisherDetailView, self).get_context_data(**kwargs)
    #     context['book_list'] = Book.objects.all()
    #     return context
    
class FillupCreateView(CreateView):
    context_object_name = "fillup"
    template_name = "fillup_new.html"
    form_class = FillupForm

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        vehicle = get_object_or_404(Vehicle, id=self.kwargs['pk'])
        kwargs['vehicle'] = vehicle
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['vehicle'] = get_object_or_404(Vehicle, id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        vehicle = get_object_or_404(Vehicle, id=self.kwargs['pk'])
        return vehicle.get_absolute_url()

@render_to('fillup_detail.html')
def fillup_detail(request, id):
    fillup = Fillup.objects.get(id=id)
    if request.method == 'POST':
        form = FillupForm(data=request.POST, instance=fillup)
        if form.is_valid():
            fillup = form.save()
    else:
        form = FillupForm(instance=fillup)
    return {'fillup': fillup, 'form': form}

