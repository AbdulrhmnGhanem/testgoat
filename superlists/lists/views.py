from django.shortcuts import render, redirect
from django.http import HttpResponse

from superlists.lists.models import Item, List


def homepage(request):

    return render(request, 'lists/homepage.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html',
                  {'items': items})


def new_list(request):

    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
