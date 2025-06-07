from django.test import TestCase
from django.urls import reverse

class MenuTests(TestCase):
    def test_get_order_submission(self):
        restaurant_id = 1  # Replace with a valid ID
        table_number = 2   # Replace with a valid table number
        
        url = reverse('menus:get_order', args=[restaurant_id, table_number])
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 200)  # Or expected status
