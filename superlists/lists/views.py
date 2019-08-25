from django.shortcuts import render, redirect
from .models import Item, List


def homepage(request):

    return render(request, 'lists/homepage.html')


def new_list(request):

    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html',
                  {'list': list_})


def add_item(request, list_id):

    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

