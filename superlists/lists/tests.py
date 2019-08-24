from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpResponse
from django.template.loader import render_to_string

from .views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        request = HttpResponse()
        response = homepage(request)
        expected_html = render_to_string('lists/homepage.html')
        self.assertEqual(response.content.decode(), expected_html)


class SmokeTest(TestCase):
    pass

    # def test_bad_math(self):
    #     self.assertEqual(1+1, 3)
