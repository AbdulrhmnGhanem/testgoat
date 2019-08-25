from pprint import pprint

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import homepage
from .models import Item


class ListViewTest(TestCase):

    def test_use_list_template(self):

        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')




class ItemModelTest(TestCase):

    def test_saving_retrieving_items(self):

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        pprint(request.POST)

    def test_homepage_redirects_after_POST(self):

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = homepage(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        #
        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'lists/homepage.html',
        #     {'new_item_text': 'A new list item'})
        # self.assertEqual(response.content.decode(), expected_html)

    def test_homepage_only_save_items_when_necessary(self):
        request = HttpRequest()
        homepage(request)
        self.assertEqual(Item.objects.count(), 0)


class SmokeTest(TestCase):
    pass

    # def test_bad_math(self):
    #     self.assertEqual(1+1, 3)
