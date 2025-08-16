from django.db import models
from menus.models import Order, Restaurant


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, null=True, blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    restaurant = models.ForeignKey(Restaurant, related_name="payments", on_delete=models.CASCADE)
    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=False)
    reference_number = models.CharField(max_length=12, unique=True, blank=False)

    @classmethod
    def get_payment(cls, reference_number):
        return cls.objects.get(reference_number=reference_number)
    
    @classmethod
    def get_latest(cls, lookup_quantity=20, starting=None):
        if not starting:
            return cls.objects.all().order_by('-payment_id')[:lookup_quantity]
        return cls.objects.all().order_by('-payment_id')[starting:lookup_quantity]
        

    def __str__(self):
        return f"Payment: (Amount: {self.amount}, escort_id: {self.escort_id}, Date: {self.timestamp})"

