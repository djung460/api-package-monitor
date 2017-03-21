from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api import handlers
from api.serializers import RequestLogSerializer, DeviceSerializer


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

    return JSONResponse(handlers.signup(data['username'], data['password'], data['phonenum'], data['deviceid']))


@csrf_exempt
def login(request):
    """
    Login a user
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    return JSONResponse(handlers.login(data['username'], data['password']))


@csrf_exempt
def acknowledge(request):
    """
    Acknowledge a request to open, can either accept or deny
    Android facing

    Returns false if there was an error
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    approved = data['approved'] == 'true' or data['approved'] == 'True'

    res = handlers.approverequest(
        data['username'],
        data['password'],
        approved)

    return JSONResponse(res)


@csrf_exempt
def viewlog(request):
    """
    View request log of a given user
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    reqs = handlers.getlog(data['username'])

    serialreqs = RequestLogSerializer(reqs, many=True)

    return JSONResponse(serialreqs.data)


@csrf_exempt
def getstatus(request):
    """
    Check if there is a pending request
    Android facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    device = handlers.getstatus(
        data['username'],
        data['password'])

    serialdevice = DeviceSerializer(device)

    return JSONResponse(serialdevice.data)


@csrf_exempt
def isack(request):
    """
    Check if the request has been acknowledged
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    print("Checking if acked")
    if handlers.isacknowledged(data['deviceid']):
        return JSONResponse('{ttttttttttttttttt}')
    else:
        return JSONResponse('{fffffffffffffffff}')


@csrf_exempt
def requestopen(request):
    """
    Called when we want to request to open the device
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    return JSONResponse(handlers.requestopen(data['deviceid'], data['image'], data['isnew'], data['done']))


@csrf_exempt
def isapproved(request):
    """
    Called once we see that the request has been acknowledged
    Device facing
    """
    if request.method != 'PUT':
        return HttpResponse(status=401)

    data = JSONParser().parse(request)

    if handlers.isapproved(data['deviceid']):
        return JSONResponse('{ttttttttttttttttt}')
    else:
        return JSONResponse('{fffffffffffffffff}')
