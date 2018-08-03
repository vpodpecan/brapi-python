from django.shortcuts import render

from pages import models


def home(request):
    try:
        homepage = models.HTML_page.objects.get(name='home')
    except models.HTML_page.DoesNotExist:
        homepage = models.HTML_page(name='home', content='')
        homepage.save()

    if not homepage.content.strip():
        content = '<h2>This page is empty. You can edit it <a href="/admin/pages/html_page/{}/change/">here</a>.</h2>'.format(homepage.pk)
    else:
        content = homepage.content
    return render(request, 'pages/home.html', {'content': content})
