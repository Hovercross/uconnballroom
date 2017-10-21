from django.db import models

from adminsortable.models import Sortable

STATUS_CHOICES = (('done', 'Done'), ('upcoming', 'Upcoming'), ('hidden', 'Hidden'))
STATUS_MAX_LENGTH = max(len(c[0]) for c in STATUS_CHOICES)

# Create your models here.
class Event(Sortable):
    class Meta(Sortable.Meta):
        pass

    name = models.CharField(max_length=254)
    note = models.CharField(max_length=254, blank=True)
    numbers = models.TextField(blank=True)
    status = models.CharField(max_length=STATUS_MAX_LENGTH, choices=STATUS_CHOICES, default='upcoming')

    def get_numbers(self):
        return list(map(str.strip, self.numbers.split()))

    def __str__(self):
        return self.name