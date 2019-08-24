from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from pprint import pprint
from .views import homepage


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_homepage_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        expected_html = render_to_string('lists/homepage.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = homepage(request)

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'lists/homepage.html',
            {'new_item_text': 'A new list item'})
        self.assertEqual(response.content.decode(), expected_html)


class SmokeTest(TestCase):
    pass

    # def test_bad_math(self):
    #     self.assertEqual(1+1, 3)
