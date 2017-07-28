from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from jsonapi import serializers, models



def index(request):
    return HttpResponse("BRAPI API")

@csrf_exempt
def germplasm_details(request, pk):
    """
    Germplasm Details by germplasmDbId
    """
    try:
        gp = models.Germplasm.objects.get(germplasmDbId=pk)
    except models.Germplasm.DoesNotExist:
        return JsonResponse('Germplasm with id {} does not exist'.format(pk), status=404)

    if request.method in ['GET', 'POST']:
        serializer = serializers.GermplasmDetailsSerializer(gp)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse(serializer.errors, status=400)
