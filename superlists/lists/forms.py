from django import forms
from .models import Item


EMPTY_LIST_ERROR = "You can't have an empty list item"


class ItemForm(forms.ModelForm):

    use_required_attribute = False

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
