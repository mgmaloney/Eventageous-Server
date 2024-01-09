from django.db import models

class Ticket(models.Model):
  event = models.ForeignKey(Event, on_delete=models.PROTECT)
  price = models.DecimalField(default=0, decimal_places=2, max_digits=6)