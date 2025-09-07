# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password, identify_hasher
# from utilities import helpers, constants
# from menus.models import Restaurant
# from django.contrib.auth.models import User

# # Create your models here

# ROLES = constants.RESTAURANT_ADMIN_ROLES

# class RestaurantAdmin(models.Model):
#     name = helpers.LowercaseTextField(max_length=50)
#     national_id = models.IntegerField()
#     phone_number = helpers.PhoneNumber(max_length=15)
#     pin = models.CharField(max_length=128, unique=True)
#     restaurant = models.ForeignKey(Restaurant, related_name='admins', on_delete=models.CASCADE)
#     role = models.CharField(max_length=10, choices=ROLES, default='waiter')
    
#     def set_pin(self, raw_pin=None):
#         if raw_pin:
#             self.pin = f"{raw_pin}{self.national_id}"
#         if not helpers.is_hashed(self.pin):
#             self.pin = make_password(self.pin)

#     def check_pin(self, raw_pin):
#         raw_pin = f"{raw_pin}{self.national_id}"
#         return check_password(raw_pin, self.pin)

#     @classmethod
#     def get(cls, raw_pin=None, restaurant=None, id=None):
#         admins = cls.objects.filter(restaurant=restaurant)
#         if id:
#             if admins:
#                 return admins.filter(id=id).first()
#             else:
#                 return cls.objects.filter(id=id).first()
#         for admin in admins:
#             if admin and admin.check_pin(raw_pin):
#                 return admin
#         return None


