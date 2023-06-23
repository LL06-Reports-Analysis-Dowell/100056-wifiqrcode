import requests
from datetime import datetime
import json
import io
from base64 import b64encode
import magic



def create_event():
    """
    This function creates an event by sending a POST request to a specified URL with various data
    parameters.
    :return: a JSON object containing the response from the API endpoint. If the status code is 201, the
    JSON object is returned. If the status code is not 201, the error message from the JSON object is
    returned.
    """

    url="https://uxlivinglab.pythonanywhere.com/create_event"
    dd = datetime.now()
    time = dd.strftime("%d:%m:%Y,%H:%M:%S")

    data={
        "platformcode":"FB" ,
        "citycode":"101",
        "daycode":"0",
        "dbcode":"pfm" ,
        "ip_address":"192.168.0.41", # get from dowell track my ip function
        "login_id":"lav", #get from login function
        "session_id":"new", #get from login function
        "processcode":"1",
        "location":"22446576", # get from dowell track my ip function
        "regional_time": time,
        "objectcode":"1",
        "instancecode":"100051",
        "context":"afdafa ",
        "document_id":"3004",
        "rules":"some rules",
        "status":"work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour":"color value",
        "hashtags":"hash tag alue",
        "mentions":"mentions value",
        "emojis":"emojis",
        "bookmarks": "a book marks"
    }

    res=requests.post(url,json=data)
    if res.status_code == 201:
        return json.loads(res.text)
    else:
        return json.loads(res.text)['error']
    

