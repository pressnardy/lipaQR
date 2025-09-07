from django.db import models
from django.contrib.auth.hashers import make_password, check_password, identify_hasher


def is_hashed(value):
    try:
        identify_hasher(value)
        return True
    except ValueError:
        return False

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