from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Item, List


class ListModelTest(TestCase):

    def test_get_absolute_url(self):

        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')


class ItemModelsTest(TestCase):

    def test_default_text(self):

        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_test(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_item(self):

        list_ = List.objects.create()
        item = Item(text='', list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_empty_list_item_to_existing_list(self):

        list_ = List.objects.create()
        item1 = Item(text='bbb', list=list_)
        item1.save()
        item1.full_clean()
        item2 = Item(text='', list=list_)

        with self.assertRaises(ValidationError):
            item2.full_clean()
            item2.save()
        self.assertEqual(Item.objects.count(), 1)

    def test_duplicate_items_are_invalid(self):

        list_ = List.objects.create()
        Item.objects.create(text='a duplicate', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='a duplicate')
            item.full_clean()

    @staticmethod
    def test_CAN_save_same_item_to_different_lists():

        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='a duplicate but on a different list')
        item = Item(list=list2, text='a duplicate but on a different list')
        item.full_clean()  # should not raise

    def test_list_ordering(self):

        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item 2')
        item3 = Item.objects.create(list=list_, text='3')

        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_representation(self):

        item = Item(text='lorem')
        self.assertEqual(repr(item), 'lorem')
