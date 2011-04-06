from django.db import models
from django.contrib.auth.models import User

import datetime

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return '"%s" - %s %s %s' % (self.name, self.year, self.make, self.model)

    @models.permalink
    def get_absolute_url(self):
        return ('vehicle_detail', (), {'pk': self.id})

    def as_a(self):
        """Returns a string <a> element that links to the car's detail page. Use |safe in templates."""
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), self.name)

    def aggregations(self):
        fillups = self.fillup_set.order_by("date")
        aggregations = fillups.aggregate(total_gallons=models.Sum('gallons'),
                                         min_odo=models.Min('odometer'),
                                         max_odo=models.Max('odometer'))
        aggregations['total_gallons'] -= fillups[0].gallons
        return aggregations

    def average_mileage(self):
        agg = self.aggregations()
        average_mileage = (agg['max_odo'] - agg['min_odo']) / agg['total_gallons']
        return "%.1f" % average_mileage
            
class Fillup(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    date = models.DateTimeField(default=datetime.datetime.now())
    odometer = models.IntegerField()
    gallons = models.DecimalField(max_digits=10, decimal_places=2)
    from_mobile = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Put %s gallons in %s on %s' % (self.gallons, self.vehicle.name, self.date)

    @models.permalink
    def get_absolute_url(self):
        return ('fillup_detail', (), {'pk': self.id})

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    date = models.DateTimeField(default=datetime.datetime.now())
    odometer = models.IntegerField(null=True, blank=True)
    MAINTENANCE_CATEGORY = (
        ('OC', 'Oil Change'),
        ('TR', 'Tire Rotation'),
        ('OF', 'Oil Filter'),
        ('AF', 'Air Filter'),
        )
    category = models.CharField(max_length=2, choices=MAINTENANCE_CATEGORY)
    notes = models.TextField(null=True, blank=True)

    def __unicode(self):
        return '%s on %s' % (self.category, self.date)
