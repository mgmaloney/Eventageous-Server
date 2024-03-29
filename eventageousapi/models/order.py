from django.db import models
from .user import User
from .payment_type import Payment_Type

class Order(models.Model):
  customer = models.ForeignKey(User, on_delete=models.PROTECT)
  payment_type = models.ForeignKey(Payment_Type, on_delete=models.PROTECT, null=True)
  total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
  billing_address = models.CharField(max_length=250, default='')
  date_completed = models.DateTimeField(blank=True, null=True)
  completed = models.BooleanField(default=False)