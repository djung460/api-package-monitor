import bcrypt
from datetime import datetime
from api.models import User, RequestLog, Device
# import the logging library
import logging
from django.conf import settings
from twilio.rest import TwilioRestClient

# Get an instance of a logger
logger = logging.getLogger(__name__)


def signup(username, password, phonenum, deviceid):
    """
    Handles put requests for signups from our Android app
    """
    # hash the password
    pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # check to see if a username is already in the database
    userexist = User.objects.filter(username=username).exists()

    if userexist:
        return "User already exists"

    user = User(
        username=username,
        pwhash=pwhash,
        phonenum=phonenum,
        deviceid=deviceid)
    user.save()

    device = Device(
        deviceid=deviceid,
        username=username,
        pendingrequest=False,
        requestgranted=False,
        imagebytes=''
    )
    device.save()

    return "User and Device added"


def login(username, password):
    """
    Handles put requests for logins from the Android app
    """
    try:
        user = User.objects.get(username=username)
        hashed = bcrypt.hashpw(password.encode('utf-8'), user.pwhash)
        return str(hashed) == str(user.pwhash)
    except User.DoesNotExist:
        return "Does not exist"


def getlog(username):
    """
    Handles retrieving the request lof associated with the user
    """
    try:
        reqs = RequestLog.objects.filter(username=username).order_by('-datetime')

        return reqs
    except RequestLog.DoesNotExist:
        return None


def getstatus(username, password):
    """
    Handles checking to see if there is a pending request
    """
    try:
        user = User.objects.get(username=username)

        if str(bcrypt.hashpw(password.encode('utf-8'), user.pwhash)) != str(user.pwhash):
            return "Password does not match"

        device = Device.objects.get(username=username)

        return device
    except User.DoesNotExist:
        return None


def approverequest(username, password, approved):
    """
    Approves device
    comes from android
    """

    try:
        user = User.objects.get(username=username)
        # check the password and deviceidr
        if (str(bcrypt.hashpw(password.encode('utf-8'), user.pwhash)) != str(user.pwhash)):
            return 'Invalid password'

        device = Device.objects.get(deviceid=user.deviceid)

        device.requestgranted = (str(approved) == 'True' or str(approved) == 'true')
        device.pendingrequest = False
        device.save()
        # Create a new request log
        rl = RequestLog(deviceid=device.deviceid, username=username, datetime=datetime.now(),
                        wasgranted=device.requestgranted,
                        imagebytes=device.imagebytes)
        rl.save()
        return 'Request acknowledged'
    except User.DoesNotExist:
        return 'Package does not exist'


def requestopen(deviceid, image, isnew, done):
    """
    Handles put requests for requesting to open the device
    comes from package monitor
    """
    print("Requesting to open")
    logger.debug("Requesting to open")

    try:
        device = Device.objects.get(deviceid=str(deviceid))
        # Begin appending the image bytes
        # that we are receiving in chunks
        if str(isnew) == 'True' or str(isnew) == 'true':
            device.imagebytes = image
            device.save()
        else:
            device.imagebytes += str(image)
            device.save()

        if str(done) == 'True' or str(done) == 'true':
            # Sent the last of the image so set pending request as true
            device.pendingrequest = True
            device.save()

            # Send the owner a text message
            user = User.objects.get(username=device.username)
            client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            client.messages.create(body="New Request! Check your app!", to="+1" + user.phonenum,
                                   from_="+14387000752")

        return "Recieved byte {} New? {} Done? {}".format(len(device.imagebytes), isnew, done)
    except Device.DoesNotExist:
        return "Device not found"


def isapproved(deviceid):
    """
    Checks to see if the request to open has been accepted
    comes from package monitor
    """
    try:
        device = Device.objects.get(deviceid=deviceid)
        return device.requestgranted
    except Device.DoesNotExist:
        return "Device not found"


def isacknowledged(deviceid):
    """
    Checks to see if the request has been accepted
    comes from package monitor
    """
    try:
        device = Device.objects.get(deviceid=deviceid)
        return not device.pendingrequest
    except Device.DoesNotExist:
        return "Device not found"
