from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return HttpResponse(b'<html><title>To-Do lists</title></html>')
