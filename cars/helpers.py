from django.db.models import Max

from cars.models import *

def xml_tag(tag, contents, header=False):
    return "%s<%s>%s</%s>" % ('<?xml version="1.0" encoding="utf-8"?>' if header else '', tag, contents, tag)

def maintenance_alerts(vehicle):
    MAINTENANCE_MILES = (
        ('OC', 3000),
        ('TR', 5000),
        ('OF', 3000),
        ('AF', 6000),
        )
    maintenances = vehicle.maintenance_set.all().values('category').annotate(most_recent_odometer=Max('odometer'))
    return maintenances
