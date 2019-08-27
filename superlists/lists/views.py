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
        return redirect(list_)


def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"
    return render(request, 'lists/list.html', {'list': list_, 'error': error})

