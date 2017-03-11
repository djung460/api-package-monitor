from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.models import PackageMonitor
from api.serializers import PackageMonitorSerializer
from api import handlers
import random


class JSONResponse(HttpResponse):
    """
    HttpResponse that renders its content to JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def signup(request):
    """
    Sign up a new user
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    if handlers.signup(data['username'],data['password'],data['phonenum'],data['deviceid']):
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=401)

@csrf_exempt
def login(request):
    """
    Login a user
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    if handlers.login(data['username'],data['password']):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)

@csrf_exempt
def acknowledge(request):
    """
    Acknowledge a request to open, can either accept or deny
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    approverequest(
            data['username'],
            data['password'],
            data['deviceid'],
            data['approved'])

@csrf_exempt
def requestcheck(request):
    """
    Check if there is a pending request
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    handlers.requestcheck(
            data['username'],
            data['password'],
            data['deviceid'])



@csrf_exempt
def isack(request):
    """
    Check if the request has been acknowledged
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    print("Checking if acked");
    return JSONResponse(handlers.isacknowledged(data['deviceid']))

@csrf_exempt
def requestopen(request):
    """
    Called when we want to request to open the device
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    if handlers.requestopen(data['deviceid'],data['image']):
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401) 


@csrf_exempt
def isapproved(request):
    """
    Called once we see that the request has been acknowledged
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    return JSONResponse(handlers.isapproved(data['deviceid'])) 
