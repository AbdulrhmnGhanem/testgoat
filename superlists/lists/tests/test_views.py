from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.test import TestCase

from superlists.lists.forms import ExistingListItemForm
from ..forms import EMPTY_LIST_ERROR
from ..views import homepage
from ..forms import ItemForm
from ..models import Item, List


class HomePageTest(TestCase):

    def test_homepage_returns_correct_html(self):

        request = HttpRequest()
        response = homepage(request)
        expected_html = render_to_string('lists/homepage.html', {'form': ItemForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_homepage_renders_home_template(self):

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/homepage.html')

    def test_homepage_use_item_form(self):

        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):

        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/homepage.html')

    def test_validation_errors_showed_on_homepage(self):

        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):

        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_item_are_not_saved(self):

        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def post_invalid_input(self):

        list_ = List.objects.create()

        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):

        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'textey'},)
        expected_error = escape("You've already got this in your list")

        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item    .objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_item_form(self):

        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_invalid_input_do_not_pass_to_db(self):

        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):

        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_invalid_input_pass_form_to_template(self):

        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_invalid_input_show_errors_on_page(self):

        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))