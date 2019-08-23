from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)


class SmokeTest(TestCase):
    pass

    # def test_bad_math(self):
    #     self.assertEqual(1+1, 3)
