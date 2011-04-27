from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

from cars.helpers import xml_tag, maintenance_alerts as m_alerts

import datetime

MAINTENANCE_CATEGORIES = (
    ('OC', 'Oil Change'),
    ('TR', 'Tire Rotation'),
    ('OF', 'Oil Filter'),
    ('AF', 'Air Filter'),
    )

MAINTENANCE_CATEGORIES_DICT = dict()
for k, v in MAINTENANCE_CATEGORIES:
    MAINTENANCE_CATEGORIES_DICT[k] = v

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)
    vin = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return '"%s" - %s %s %s' % (self.name, self.year, self.make, self.model)

    @models.permalink
    def get_absolute_url(self):
        return ('vehicle_detail', (), {'pk': self.id})

    def as_a(self):
        """Returns a string <a> element that links to the car's detail page. Use |safe in templates."""
        return '<a href="%s">%s</a>' % (self.get_absolute_url(), self.name)

    def as_xml(self, header=False):
        contents = ''
        contents += xml_tag('id', self.pk)
        contents += xml_tag('make', self.make)
        contents += xml_tag('model', self.model)
        contents += xml_tag('year', self.year)
        contents += xml_tag('name', self.name)
        contents += xml_tag('description', self.description)
        contents += xml_tag('owner', self.owner)
        contents += xml_tag('vin', self.vin)
        contents += xml_tag('mileage', self.average_mileage())
        contents += xml_tag('carbon', self.carbon_footprint())
        maint_tags = ''
        for alert in self.maintenance_alerts():
            maint_tag = ''
            maint_tag += xml_tag('category', alert['category_full'])
            maint_tag += xml_tag('due_when_odometer_at', alert['due_at'])
            maint_tags += xml_tag('alert', maint_tag)
        contents += xml_tag('maintenance_alerts', maint_tags)
        return xml_tag('vehicle', contents, header=header)

    def aggregations(self):
        fillups = self.fillup_set.order_by("date")
        aggregations = fillups.aggregate(total_gallons=models.Sum('gallons'),
                                         min_odo=models.Min('odometer'),
                                         max_odo=models.Max('odometer'))
        if len(fillups) > 1:
            aggregations['total_gallons'] -= fillups[0].gallons
        return aggregations

    def average_mileage(self):
        agg = self.aggregations()
        if self.fillup_set.count() >= 2 and agg['total_gallons'] != 0:
            average_mileage = (agg['max_odo'] - agg['min_odo']) / agg['total_gallons']
        else:
            average_mileage = None
        return "%.1f" % average_mileage

    def carbon_footprint(self):
        """Returns a tuple of (number, unit) where both number and unit are strings."""
        gallons = self.aggregations()['total_gallons']
        co2 = float(gallons) * 19.4
        # This conditional number/unit crap sucks and is probably wrong
        if co2 > 1000000:
            number = "%.1f" % (co2 / 2000000) + "k"
            unit = "tons"
        elif co2 > 1000:
            number = "%.1f" % (co2 / 1000) + "k"
            if co2 > 100000:
                number = "%.0f" % (co2 / 1000) + "k"
            unit = "lb"
        else:
            number = "%.0f" % co2
            unit = "lb"
        return (number, unit)

    def most_recent_odometer(self):
        return self.fillup_set.aggregate(max=Max('odometer'))['max']

    def maintenance_alerts(self, show_all=False):
        """Returns a list of dictionaries representing the most recent of each category of maintenance report. If show_all=True, it will return all categories, otherwise it will return upcoming ones."""
        alerts = m_alerts(self)
        for alert in alerts:
            alert['category_full'] = MAINTENANCE_CATEGORIES_DICT[alert['category']]
            alert['due_at'] = alert['most_recent_odometer'] + 3000
        mro = self.most_recent_odometer()
        if show_all:
            upcoming_alerts = [alert for alert in alerts]
        else:
            upcoming_alerts = [alert for alert in alerts if alert['due_at'] < mro + 500]
        return upcoming_alerts

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
    category = models.CharField(max_length=2, choices=MAINTENANCE_CATEGORIES)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s on %s' % (self.category, self.date)
