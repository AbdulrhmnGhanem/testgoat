from django.test import TestCase

from ..forms import ItemForm, EMPTY_LIST_ERROR


class ItemFormTest(TestCase):

    def test_from_renders_text_input(self):

        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-group-lg"', form.as_p())

    def test_form_validation_for_blank_item(self):

        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],[EMPTY_LIST_ERROR])
