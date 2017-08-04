from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from jsonapi import serializers, models

DEF_PAGE_SIZE = 1000
HTTP_BAD_REQUEST_CODE = 400
#
#
# @csrf_exempt
# def germplasm_details(request, pk):
#     """
#     Germplasm Details by germplasmDbId
#     """
#     try:
#         gp = models.Germplasm.objects.get(germplasmDbId=pk)
#     except models.Germplasm.DoesNotExist:
#         return JsonResponse('Germplasm with id {} does not exist'.format(pk), status=404)
#
#     gp = models.Germplasm.objects.all()
#     if request.method in ['GET', 'POST']:
#         serializer = serializers.GermplasmDetailsSerializer(gp, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     else:
#         return JsonResponse(serializer.errors, status=400)
#
#


#
#
#
# def buildResponse(**kwargs):
#     out = {}
#
#
#
#  {
#       "metadata" : {
#            "pagination": {
#               "pageSize":0,
#               "currentPage":0,
#               "totalCount":0,
#               "totalPages":0
#           },
#           "status" : [ {
#               "message": "Unable to parse POST request",
#               "code" : ""
#           } ],
#           "datafiles": []
#       },
#       "result": {}
#   }



class JSONResponseMixin(object):
    def buildErrorResponse(self, message, code):
        err = {"metadata": {
                "pagination": {
                    "pageSize": 0,
                    "currentPage": 0,
                    "totalCount": 0,
                    "totalPages": 0
                },
                "status": [{
                    "message": message,
                    "code": code
                }],
                "datafiles": []
            },
            "result": {}
        }
        return err

    def buildResponse(self, results, pagination={"pageSize": 0, "currentPage": 0, "totalCount": 0, "totalPages": 0}, status=[], datafiles=[]):
        output = {}
        output['result'] = results
        output['pagination'] = pagination
        output['status'] = status
        output['datafiles'] = datafiles
        return output

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        # sanity: fail if there are unwanted parameters
        extra = set(self.request.GET.keys()) - set(self.query_parameters) - set(['page', 'pageSize'])
        if extra != set():
            return self.buildErrorResponse('Invalid query pararameter(s) {}'.format(extra), HTTP_BAD_REQUEST_CODE)

        # 1. construct query
        kwargs = {}
        for param in self.query_parameters:
            val = self.request.GET.get(param)
            if val:
                kwargs[param] = val

        # print(kwargs)
        # 2. execute query and make pagination
        # objects = models.Program.objects.filter(**kwargs)
        objects = self.model.objects.filter(**kwargs)
        try:
            pagesize = int(self.request.GET.get('pageSize', DEF_PAGE_SIZE))
            page = int(self.request.GET.get('page', 0)) + 1  # BRAPI wants zero page indexing...
        except:
            return self.buildErrorResponse('Invalid page or pageSize parameter', HTTP_BAD_REQUEST_CODE)

        paginator = Paginator(objects, pagesize)
        try:
            pageObjects = paginator.page(page)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            return self.buildErrorResponse('Empty page was requested: {}'.format(page-1), HTTP_BAD_REQUEST_CODE)
            # pageObjects = paginator.page(paginator.num_pages)
        pagination = {'pageSize': pagesize,
                      'currentPage': page-1,
                      'totalCount': len(objects),
                      'totalPages': paginator.num_pages
                      }

        # 3. return serialized data
        data = []
        for obj in pageObjects:
            data.append(self.serializer(obj).data)
        return self.buildResponse(results={'data': data}, pagination=pagination)
# end


class JSONResponseMixinDetails(JSONResponseMixin):
    def get_data(self, context):
        try:
            pkval = self.kwargs.get(self.pk)
            obj = self.model.objects.get(pk=pkval)
        except self.model.DoesNotExist:
            return self.buildErrorResponse('Invalid object ID', 404)

        serializer = self.serializer(obj)
        return self.buildResponse(results=serializer.data)


class Index(TemplateView):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        return HttpResponse("BRAPI API")


class GermplasmDetails(JSONResponseMixinDetails, TemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    pk = 'germplasmDbId'


class GermplasmSearch(JSONResponseMixin, TemplateView):
    model = models.Germplasm
    serializer = serializers.GermplasmDetailsSerializer
    query_parameters = ['germplasmName', 'germplasmDbId', 'germplasmPUI']


class ProgramList(JSONResponseMixin, TemplateView):
    model = models.Program
    serializer = serializers.ProgramSerializer
    query_parameters = ['programName', 'abbreviation']


class TrialDetails(JSONResponseMixinDetails, TemplateView):
    model = models.Trial
    serializer = serializers.TrialDetailsSerializer
    pk = 'trialDbId'
