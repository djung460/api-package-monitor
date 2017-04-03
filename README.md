# api-package-monitor
API for our Home Package Monitor project

## USAGE

### Mobile Facing
#### Sign up
http --json put http://host/api/signup username=username password=password phonenum=phonenumber deviceid=deviceid
#### Login
http --json put http://host/api/login username=username password=password
#### Acknowledge - Acknowledges a request
http --json put http://host/api/acknowledge username=username password=password deviceid=deviceid approved=boolean
#### Check pending - Returns device info for if the device has a pending request (Should be called before getstatus)
http --json put http://host/api/checkpending username=username password=password deviceid=deviceid
#### Get owned devices - Returns devices and their status owned by the user
http --json put http://host/api/viewdevices username=username
#### Get status - Returns device info
http --json put http://host/api/getstatus username=username password=password deviceid=deviceid
#### Add a device - Adds a device to a user
http --json put http://host/api/adddevice username=username deviceid=deviceid
#### Remove a device - Removes a device from a user
http --json put http://host/api/removedevice username=username deviceid=deviceid
#### View Requests Log - Returns log of device
http --json put http://host/api/viewlog username=username deviceid=deviceid
