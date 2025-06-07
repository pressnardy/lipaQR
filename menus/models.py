from django.db import models


# Create your models here.
class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=100)
    restaurant_location = models.CharField(max_length=100)
    till_number = models.IntegerField(null=True)
    
    @property
    def menu(self):
        return self.items.filter(available=True)

    def __str__(self):
        return f"{self.restaurant_name}: {self.restaurant_location}"


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255, blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_image = models.FileField(upload_to='item_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item_name}: {self.item_price}"

            
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    reference_number = models.CharField(unique=True)
    table_number = models.IntegerField(null=True)
    phone_number = models.IntegerField(null=True)
    restaurant = models.ForeignKey(Restaurant, related_name="orders", on_delete=models.CASCADE)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order No: {self.order_id} | Ref. No: {self.reference_number} " \
               f"| Restaurant: {self.restaurant.restaurant_name} | Amount: {self.total_amount}"

    @staticmethod
    def latest_pending(phone_number):
        return Order.objects.filter(phone_number=phone_number, paid=False).order_by('-order_id').first()

    @staticmethod
    def latest_paid(phone_number):
        return Order.objects.filter(phone_number=phone_number, paid=True).order_by('-order_id').first()

    @property
    def items(self):
        return self.ordered_items.all()
    

class OrderedItem(models.Model):
    ordered_item_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="orders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_items")
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.item is not None:
            self.total = self.item.item_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item: {self.item.item_name} | Price: {self.item.item_price} | Quantity: {self.quantity}"
