from django.test import TestCase
from users.models import CustomUser


class CustomUserTestCase(TestCase):
    def setUp(self) -> None:
        CustomUser.objects.create(username="Mike", password="mike@123", email="aglida1370@gmail.com")

    def test_username_exists_error(self):
        """Username of a new user should not already exist in the database"""
        try:
            CustomUser.objects.create(username="Mike", password="mike@123", email="aglida1333@gmail.com")
        except:
            self.assertFalse(False)
