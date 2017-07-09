from django.db import models

from registration.models import Person

# Create your models here.
class Costume(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=12, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Maintenance(models.Model):
    costume = models.ForeignKey(Costume)
    maintenance_date = models.DateField()
    did_clean = models.BooleanField()
    did_rhinestone = models.BooleanField()
    did_sew = models.BooleanField()
    notes = models.TextField(blank=True)
    fixer = models.ForeignKey(Person)

    def __str__(self):
        costume_name = self.costume.name
        formatted_date = self.maintenance_date.strftime("%Y-%m-%d")

        s = "{} on {}".format(costume_name, formatted_date)
        return s
