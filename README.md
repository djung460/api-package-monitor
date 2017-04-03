# api-package-monitor
API for our Home Package Monitor project

## USAGE

### Mobile Facing
#### Sign up
http --json put http://host/api/signup username=username password=password phonenum=phonenumber deviceid=deviceid
#### Login
http --json put http://host/api/login username=username password=password
#### Acknowledge - Acknowledges a request
http --json put http://host/api/acknowledge username=username password=password approved=boolean
### Check pending - Returns device info for if the device has a pending request (Should be called before getstatus)
http --json put http://host/api/checkpending username=username password=password
#### Get status - Returns device info
http --json put http://host/api/getstatus username=username password=password
#### View Requests Log - Returns log of device
http --json put http://host/api/viewlog username=username
