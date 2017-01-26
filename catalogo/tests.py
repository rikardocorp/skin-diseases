import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Category
# Create your tests here.


class CategoryMethodTests(TestCase):

    def test_was_published_recently_with_future_category(self):

        time = timezone.now() + datetime.timedelta(days=30)
        future_category = Category(pub_date=time)
        self.assertIs(future_category.was_published_recently(), False)

    def test_was_published_recently_with_old_category(self):

        time = timezone.now() + datetime.timedelta(days=30)
        old_category = Category(pub_date=time)
        self.assertIs(old_category.was_published_recently(), False)

    def test_was_published_recently_with_recent_category(self):

        time = timezone.now() - datetime.timedelta(hours=1)
        recent_category = Category(pub_date=time)
        self.assertIs(recent_category.was_published_recently(), True)