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
        output['metadata'] = {}
        output['metadata']['pagination'] = pagination
        output['metadata']['status'] = status
        output['metadata']['datafiles'] = datafiles
        return output

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_post_or_get(self, request):
        # we will handle both types of requests for all calls
        # simulate depretaced request.REQUEST
        return request.POST or request.GET

    def get_objects(self, kwargs):
        objects = self.model.objects.filter(**kwargs)
        return objects

    def get_data(self, context):
        request = self.get_post_or_get(self.request)

        # sanity: fail if there are unwanted parameters
        extra = set(request.keys()) - set(self.query_parameters) - set(['page', 'pageSize'])
        if extra != set():
            return self.buildErrorResponse('Invalid query pararameter(s) {}'.format(extra), HTTP_BAD_REQUEST_CODE)

        # 1. construct query
        kwargs = {}
        for param in self.query_parameters:
            val = request.get(param)
            if val:
                kwargs[param] = val
        # print(kwargs)

        # 2. execute query and make pagination
        objects = self.get_objects(kwargs)
        # try:
        #     objects = self.get_objects(kwargs)
        # except Exception as e:
        #     return self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE)

        # try:
        #     objects = self.model.objects.filter(**kwargs)
        # except Exception as e:
        #     return self.buildErrorResponse('Data error: {}'.format(str(e)), HTTP_BAD_REQUEST_CODE)

        try:
            pagesize = int(request.get('pageSize', DEF_PAGE_SIZE))
            page = int(request.get('page', 0)) + 1  # BRAPI wants zero page indexing...
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


class TrialList(JSONResponseMixin, TemplateView):
    model = models.Trial
    serializer = serializers.TrialDetailsSerializer
    query_parameters = ['programDbId', 'locationDbId', 'active', ]

    def get_objects(self, kwargs):
        if 'locationDbId' in kwargs:
            studies = models.Study.objects.filter(locationDbId=kwargs['locationDbId'])
            # objects = 

            models.Trial.objects.filter(locationDbId__in=studies)
        else:
            objects = self.model.objects
        return objects.filter(**kwargs)

#objects = self.model.objects.filter(**kwargs)
#     studies = models.Study.objects.filter(locationDbId=locationDbId)
#     trials = models.Trial.objects.filter()
