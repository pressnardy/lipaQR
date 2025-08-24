from django.db import models
from django.contrib.auth.models import User
from dotenv import load_dotenv


load_dotenv()

class LowercaseTextField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is None:
            return value
        if not isinstance(value, str):
            value = str(value)
        return value.lower().strip()

class PhoneNumber(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is None:
            return value
        return f"0{value[-9:]}"


# Create your models here.
class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = LowercaseTextField(max_length=100, null=True, blank=False)
    location = LowercaseTextField(max_length=50, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=False)
    phone_number = PhoneNumber(max_length=15, null=True, blank=False)
    till_number = models.IntegerField(null=True, blank=False)
    created_by = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    @property
    def menu(self):
        return self.items.filter(available=True)
    
    def all_items(self):
        return self.items.all()
    

    def in_menu(self, item_name=None, item_id=None):
        if item_name:
            if item := self.items.filter(available=True, name=item_name).first():
                return True
        if item_id:
            if item := self.items.filter(available=True, item_id=item_id).first():
                return True
        return False
        
        
    def new_orders(self):
        all_orders = self.orders.filter(new=True).order_by('order_id')
        paid = self.orders.filter(paid=True, new=True).order_by('-order_id')
        pending = self.orders.filter(paid=False, new=True).order_by('-order_id')
        return {'paid': paid, 'pending': pending, 'all':all_orders}
    

    def paid_orders(self, quantity=-1):
        return self.orders.filter(paid=True).order_by('-order_id')[:quantity]
    
    def pending_orders(self, quantity=-1):
        return self.orders.filter(paid=False).order_by('-oder_id')[:quantity]
    
    def items_unavailable(self):
        return self.items.filter(available=False)
    
    @classmethod
    def update_phones(cls):
        rests = cls.objects.all()
        for i in rests:
            i.phone_number = f"0{i.phone_number[-9:]}"
            i.save()

    def __str__(self):
        return f"{self.name}: {self.location}"


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = LowercaseTextField(max_length=100, null=True, blank=False)
    description = models.CharField(max_length=255, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='item_images/', blank=False, null=True)
    available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)

    @classmethod
    def get(cls, item_id):
        return cls.objects.filter(item_id=item_id).first()
        
    @classmethod
    def is_available(cls, item_id):
        if item := cls.get(item_id):
            return item.available
        return False

    def __str__(self):
        return f" {self.item_id} | {self.name} | {self.unit} | {self.unit_price}"
        
            
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    reference_number = models.CharField(unique=True, max_length=20)
    table_number = models.IntegerField(null=True, blank=False)
    phone_number = PhoneNumber(max_length=15, null=True, blank=False)
    restaurant = models.ForeignKey(Restaurant, related_name="orders", on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True, default=None)
    paid = models.BooleanField(default=False)
    new = models.BooleanField(default=True)

    @classmethod
    def get(cls, unique_value):
        if isinstance(unique_value, int):
            if order := cls.objects.filter(order_id=unique_value).first():
                return order
        if order := cls.objects.filter(reference_number=unique_value).first():
            return order
        if order := cls.objects.filter(phone_number=unique_value).order_by('-order_id').first():
            return order
        return None
    
    @property
    def items_ordered(self):
        return self.ordered_items.all()

    def items_available(self):
        # try:
        return [item for item in self.ordered_items.all() if item.is_available]
        # except ValueError:
        #     pass

    def items_unavailable(self):
        return [item for item in self.ordered_items.all() if not item.is_available]

    def total(self):
        if self.items_available():
            self.total_amount = sum(item.total for item in self.items_available())
        return self.total_amount
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total()
        super().save(*args, **kwargs)
    
    @property
    def is_paid(self):
        return self.paid
    
    def mark_paid(self):
        for item in self.items:
            item.paid = True
            item.save()
        self.paid = True
        self.save()

    @classmethod
    def latest_pending(cls, phone_number=None):
        """
        Identifies the customer by the phone number if provided,
        Aassumes the latest order placed is the valid one.
        """
        if phone_number:
            return cls.objects.filter(phone_number=phone_number, paid=False).order_by('-order_id').first()
        return cls.objects.filter(paid=False).order_by('-order_id').first()


    @classmethod
    def latest_paid(cls, phone_number):
        return cls.objects.filter(phone_number=phone_number, paid=True).order_by('-order_id').first()

    @classmethod
    def update_phones(cls):
        orders = cls.objects.all()
        for i in orders:
            i.phone_number = f"0{i.phone_number[-9:]}"
            i.save()
            
    def __str__(self):
        return f"Order No: {self.order_id} | Ref. No: {self.reference_number} " \
               f"| Amount: {self.total_amount}"


class OrderedItem(models.Model):
    ordered_item_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="orders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_items")
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    paid = models.BooleanField(default=False)

    def is_available(self):
        return self.item.available

    @classmethod
    def add(cls, item, order, quantity):
        if isinstance(item, Item) and isinstance(order, Order):
            obj = cls.objects.create(item, order, quantity)
            obj.save()

    @classmethod
    def set_to_paid(cls, ordered_item_id):
        if obj := cls.objects.get(ordered_item_id):
            obj.paid = True     
            obj.save()

    @classmethod
    def add_items(cls, ordered_items, order:Order):
        """can take a single item object or a list of objects"""
        ordered_items = list(ordered_items)
        for i in ordered_items:
            cls.add(item=i['item'], order=order, quantity=i['quantity'])

    def save(self, *args, **kwargs):
        if self.item is not None:
            self.total = self.item.unit_price * self.quantity
            super().save(*args, **kwargs)
        else:
            raise TypeError('ITEM CANNOT BE NONE')

    def __str__(self):
        return f"{self.ordered_item_id} | Item: {self.item.name} | Price: {self.item.unit_price} | Quantity: {self.quantity}"


class ItemImage(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, related_name='images', null=True)
    image_field = models.FileField(upload_to='item_images/') 



