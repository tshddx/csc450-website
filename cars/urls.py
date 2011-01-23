from django.conf.urls.defaults import *
from csc450.cars.models import *

urlpatterns = patterns('csc450.cars.views',
                       # Nothing yet.
)

urlpatterns += patterns('django.views.generic',
                        url(regex=r'^$',
                            view='simple.direct_to_template',
                            kwargs={'template': 'base.html'},
                            name='index'
                        ),
)

