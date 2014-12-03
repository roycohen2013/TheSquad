
import requests
import json
from requests.auth import HTTPBasicAuth


def sendText(toNumber, Content):

    toNumber = "+1" + toNumber 
    smsURL  =  "https://v1.api.phone.com/sms"
    username =  "eeb2cc16-88ef-11e3-9dfc-f9a580011ac9"
    Password =  "Myg6Um3Up"
    FromNumber = "+15162094696"   # default assigned from phone.com


    headers = {'content-type': 'application/json'}
    payload = { 'from': FromNumber, 'to': toNumber,'message': Content }

    auth = HTTPBasicAuth(username, Password) 

    r = requests.post(smsURL, data=json.dumps(payload), headers=headers,auth=auth)

    print (r.text)




# bulkMessage = "This is your friendly neighborhood toolCloud server reminding you all that texting functionality is now up and running"


# sendText("9176905094", bulkMessage)
# sendText("2404697313", bulkMessage)
# sendText("2032097215", bulkMessage)
# sendText("3154805597", bulkMessage)
# sendText("6176803278", bulkMessage)
# sendText("2482292139", bulkMessage)





 