import bcrypt
from datetime import datetime
from api.models import PackageMonitor, RequestLog
from api.serializers import PackageMonitorSerializer

def signup(username, password, phonenum, deviceid):
    """
    Handles put requests for signups from our Android app
    """
    # hash the password
    pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # hash the device id
    didhash = bcrypt.hashpw(deviceid.encode('utf-8'), bcrypt.gensalt())
    # check to see if a username is already in the database
    userexist = PackageMonitor.objects.filter(username=username).exists()

    if userexist:
        return False

    pm = PackageMonitor(
            username=username, 
            pwhash=pwhash, 
            phonenum=phonenum, 
            didhash=didhash,
            pendingrequest=False,
            requestgranted=False)
    
    print(pm.username)
    print(pm.pwhash)
    print(pm.phonenum)
    print(pm.didhash)
    print(pm.pendingrequest)
    print(pm.requestgranted)
    pm.save()

    return True

def login(username, password):
    """
    Handles put requests for logins from the Android app
    """
    try:
        pm = PackageMonitor.objects.get(username=username)

        return bcrypt.hashpw(password.encode('utf-8'), pm.pwhash) == pm.pwhash

    except PackageMonitor.DoesNotExist:
        return False

def requestcheck(username, password, deviceid):
    """
    Handles checking to see if there is a pending request
    """
    try:
        pm = PackageMonitor.objects.get(username=username)

        if bcrypt.hashpw(password.encode('utf-8'), pm.pwhash) != pm.pwhash:
            return False
        if(bcrypt.hashpw(deviceid.encode('utf-8'), pm.deviceid) != pm.deviceid):
            return False

        return pm.pendingrequest
    except PackageMonitor.DoesNotExist:
        return False


def approverequest(username, password, deviceid, approved):
    """
    Approves device
    comes from android
    """
    
    try:
        pm = PackageMonitor.objects.get(username=username)
        # check the password and deviceid
        if(bcrypt.hashpw(password.encode('utf-8'), pm.pwhash) != pm.pwhash):
            return False
        if(bcrypt.hashpw(deviceid.encode('utf-8'), pm.deviceid) != pm.deviceid):
            return False

        pm.requestgranted = approved
        pm.pendingrequest = False
        pm.save()
        #Create a new request log
        rl = RequestLog.objects.get(username=pm.username).latest()
        rl.wasgranted = approved
        rl.save()
    except PackageMonitor.DoesNotExist:
        return false

def getprevreqs(username, password, deviceid):
    """
    Retrieves the request log of the user
    comes from android
    """
    
    try:
        pm = PackageMonitor.objects.get(username=username)
        # check the password and deviceid
        if(bcrypt.hashpw(password.encode('utf-8'), pm.pwhash) != pm.pwhash):
            return False
        if(bcrypt.hashpw(deviceid.encode('utf-8'), pm.deviceid) != pm.deviceid):
            return False

        return RequestLog.objects.get(username=username)

    except PackageMonitor.DoesNotExist:
        return null



def requestopen(deviceid, image):
    """
    Handles put requests for requesting to open the device
    comes from package monitor
    """
    print("Requesting to open")
    for pm in PackageMonitor.objects.all():
        # go through each entry and check the device ids
        if bcrypt.hashpw(deviceid.encode('utf-8'), pm.didhash) == pm.didhash:
            pm.pendingrequest = True
            #Add the photo to the database

            #Send a push notification here

            #User then should ask for the latest photo from their device
            pm.save()

            #Create a new request log
            rl = RequestLog(
                    username=pm.username,
                    didhash=pm.didhash,
                    datetime=datetime.now(),
                    wasgranted=False,
                    imagebytes=image)
            rl.save()

            return True

    # device not in the database
    return False

def isapproved(deviceid):
    """
    Checks to see if the request to open has been accepted
    comes from package monitor
    """
    for pm in PackageMonitor.objects.all():
        # go through each entry and check the device ids
        if bcrypt.hashpw(deviceid.encode('utf-8'), pm.didhash) == pm.didhash:
            return pm.requestgranted

    # shouldn't reach here since at this point since this case handled before
    return False

def isacknowledged(deviceid):
    """
    Checks to see if the request has been accepted
    comes from package monitor
    """
    for pm in PackageMonitor.objects.all():
        # go through each entry and check the device ids
        if bcrypt.hashpw(deviceid.encode('utf-8'), pm.didhash) == pm.didhash:
            print("Device has been acknowledged")
            return not pm.pendingrequest

    print("Device not found")
    # shouldn't reach here since at this point since this case handled before
    return False
