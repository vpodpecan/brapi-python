from django.shortcuts import render

from homepage import models


def home(request):
    return render(request, 'homepage/home.html', {'data': models.RichText.objects.get(name='homepage')})
