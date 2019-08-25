from django.shortcuts import render, redirect
from django.http import HttpResponse

from superlists.lists.models import Item


def homepage(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    items = Item.objects.all()
    return render(request, 'lists/homepage.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html',
                  {'items': items})
