from django.db import models

class User(models.Model):
    # Email of the owner
    username = models.TextField(primary_key=True)
    # Owner's password hashed
    pwhash = models.BinaryField()
    # phone number of owner
    phonenum = models.TextField()
    # device
    deviceid = models.TextField()

class Device(models.Model):
    deviceid = models.TextField(primary_key=True)
    # currently support one to one
    username = models.TextField()
    # set this to true when request made
    pendingrequest = models.BooleanField()
    # set this to true when the request granted
    requestgranted = models.BooleanField()
    # image bytes
    imagebytes = models.TextField()

class RequestLog(models.Model):
    # user the log belongs to
    username = models.TextField()
    # device id
    deviceid = models.TextField()
    # date and time requested
    datetime = models.DateTimeField()
    # result of request
    wasgranted = models.BooleanField()
    # bytes of jpeg image
    imagebytes = models.TextField()



