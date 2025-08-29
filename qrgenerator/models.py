from django.db import models
from menus.models import Restaurant


class QrImage(models.Model):
    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='qr_codes')
    image_field = models.FileField(upload_to="qr_codes/", null=False)  # Use FileField instead of FieldFile

    class Meta:
        unique_together = ('table_number', 'restaurant')

    @classmethod
    def add(cls, table_number, restaurant_id):
        restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
        if not Restaurant:
            return
        
        obj, created = cls.objects.update_or_create(
            table_number=table_number,
            restaurant=restaurant,
        )
        return obj

    @property
    def url(self):
        return self.image_field.url
    
    def __str__(self):
        return f"Table: {self.table_number} | Image: {self.image_field} |url: {self.url}"
