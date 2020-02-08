from django.views.generic.base import TemplateView
from django.shortcuts import render


class TestView(TemplateView):
    template_name = "index.html"


def index(request):
    return render(request, 'chat_index.html', {})


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })
