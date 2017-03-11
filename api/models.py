from django.db import models

class PackageMonitor(models.Model):
    # Email of the owner
    username = models.TextField(primary_key=True)
    # Owner's password hashed
    pwhash = models.BinaryField()
    # phone number of owner
    phonenum = models.TextField()
    # device ID
    didhash = models.BinaryField()
    # pending request
    pendingrequest = models.BooleanField()
    # accept request
    requestgranted = models.BooleanField()

class RequestLog(models.Model):
    # user the log belongs to
    username = models.TextField()
    # device id
    didhash = models.TextField()
    # date and time requested
    datetime = models.DateTimeField()
    # result of request
    wasgranted = models.BooleanField()
    # bytes of jpeg image
    imagebytes = models.TextField()
