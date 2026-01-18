from django.shortcuts import render


def index(request):
    return render(request, 'sending_messages/base.html')
