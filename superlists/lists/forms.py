from django import forms
from django.core.exceptions import ValidationError
from .models import Item


EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.ModelForm):

    use_required_attribute = False

    # noinspection PyMethodOverriding
    def save(self, for_list):
        """

        :type for_list: List
        """
        self.instance.list = for_list
        return super().save()

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-group-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.ModelForm.save(self)
