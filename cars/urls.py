from django.conf.urls.defaults import *
from django.views.generic import *
from cars.models import *
from cars.views import *

urlpatterns = patterns('cars.views',
                       url(regex=r'^register$',
                           view='user_register',
                           name='user_register'
                           ),
                       url(regex=r'^login$',
                           view='user_login',
                           name='user_login'
                           ),
                       url(regex=r'^logoff$',
                           view='user_logoff',
                           name='user_logoff'
                           ),
                       url(regex=r'^dashboard$',
                           view='dashboard',
                           name='dashboard'
                           ),
                       url(regex=r'^vehicle/add$',
                           view='add_car',
                           name='add_car'
                           ),
                       url(regex=r'^vehicle/(?P<pk>[0-9]*)$',
                           view=VehicleUpdateView.as_view(),
                           name='vehicle_detail',
                           ),
                       url(regex=r'^vehicle/(?P<pk>[0-9]*)/fillup/new$',
                           view=FillupCreateView.as_view(),
                           name='fillup_new'
                           ),
                       url(regex=r'fillup/(?P<pk>[0-9]*)^$',
                           view='fillup_detail',
                           name='fillup_detail'
                           ),
                       url(regex=r'api/vehiclelist$',
                           view='api_vehicle_list',
                           name='api_vehicle_list'
                           ),
                       url(regex=r'api/fillup$',
                           view='api_fillup_create',
                           name='api_fillup_create'
                           ),
                       url(regex=r'api/vehicle$',
                           view='api_vehicle_detail',
                           name='api_vehicle_detail'
                           ),
                       
                       # Site root
                       url(regex=r'^$',
                           view='index',
                           name='index'
                           ),
)

urlpatterns += patterns('django.views.generic',

)

