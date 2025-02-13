from django.test import TestCase

from superlists.lists.models import Item
from ..models import List
from ..forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_LIST_ERROR,
    ExistingListItemForm, ItemForm
)


class ExistingListItemFormTest(TestCase):

    def test_from_renders_text_input(self):

        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)

        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_item(self):

        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_validation_for_duplicate_items(self):

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


class ItemFormTest(TestCase):

    def test_from_renders_text_input(self):

        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-group-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):

        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR])

    def test_form_save_handle_saving_to_list(self):

        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)
