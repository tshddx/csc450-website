from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return "%s %s %s owned by %s" % (self.year, self.make, self.model, self.owner)
