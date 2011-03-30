from django.conf.urls.defaults import *
from cars.models import *

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
                       url(regex=r'^car/(?P<id>[0-9]*)$',
                           view='car_detail',
                           name='car_detail',
                           ),
                       url(regex=r'^add$',
                           view='add_car',
                           name='add_car'
                           ),
                       url(regex=r'^$',
                           view='index',
                           name='index'
                           ),
)

urlpatterns += patterns('django.views.generic',

)

