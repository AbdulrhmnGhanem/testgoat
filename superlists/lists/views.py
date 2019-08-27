from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .models import Item, List


def homepage(request):

    return render(request, 'lists/homepage.html')


def new_list(request):

    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)

    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        expected_error = "You can't have an empty list item"
        return render(request, 'lists/homepage.html', {'error': expected_error})
    else:
        return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')
    return render(request, 'lists/list.html', {'list': list_})

