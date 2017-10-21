from django.db import models

from adminsortable.models import Sortable

# Create your models here.
class Event(Sortable):
    class Meta(Sortable.Meta):
        pass

    name = models.CharField(max_length=254)
    note = models.CharField(max_length=254, blank=True)
    numbers = models.TextField(blank=True)
    show = models.BooleanField(default=True)

    def get_numbers(self):
        return list(map(str.strip, self.numbers.split()))

    def __str__(self):
        return self.name