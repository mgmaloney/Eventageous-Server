from django.db import models
from .event import Event

class Ticket(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_ticket')
  price = models.DecimalField(default=0, decimal_places=2, max_digits=6)