from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import qrcode 
from django.conf import settings
import os
from PIL import Image
from django.templatetags.static import static
import string
import random
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .utils import create_event
from datetime import datetime
import requests

@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):

    def get(self, request):
        return Response({"info": "Welcome to Dowell-wifi-qrcode-app"},status=status.HTTP_200_OK)

# This class generates a QR code for a WiFi network and saves it to a database.
class GenerateWifiQr(APIView):
    """
    Generates Quick Response Code for a Wifi Network
    
    """
    

    def get(self, request, format=None):
        
        """Returns a list of APIView features"""
        an_apiview = {
            'wifi_name': 'Name / SSID of the WIFI Network',
            'wifi_password': 'Password of the wifi ',
            'encryption_type': 'Either WPA (for WPA and WPA2) or WEP or nopass if no encryption type is available'
        }
            

        return Response({'payload description': an_apiview})
    
    def post(self, request):
        """
        This function generates a QR code image with wifi credentials and saves it to a database, and also
        creates a new user for the QR code.
        
        :param request: The HTTP request object containing metadata about the request, such as headers and
        data
        :return: a Response object with a JSON payload containing a success flag, a dictionary of returned
        data, and an HTTP status code.
        """
        try: 
            wifi_name = request.data['wifi_name']
            wifi_password = request.data['wifi_password']
            encryption_type =  request.data['encryption_type'].upper()

            dd = datetime.now()
            time = dd.strftime("%H:%M:%S")
            date = dd.strftime("%d:%m:%Y")


            if encryption_type == "" or encryption_type.lower() == "none" or encryption_type.lower() =="nopass":
                encryption_type == "nopass"
            elif "wpa" in encryption_type.lower() or "wpa2" in encryption_type.lower():
                encryption_type = "WPA"
            elif "wep" in encryption_type.lower():
                encryption_type = "WEP"
            else:
                return Response({"message": "Invalid Encryption type", "success": False}, status=HTTP_400_BAD_REQUEST)

            data = f"WIFI:T:{encryption_type};S:{wifi_name};P:{wifi_password};;"

            # generating a QR code image using the `qrcode` library in Python.
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make()

            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            #adding logo to the qr code
            logo_name = "logo.jpg"
            image_path = f"{settings.BASE_DIR}/static/{logo_name}"
            image = Image.open(image_path)
            image_width, image_height = image.size

            max_size = min(qr_img.size) // 5

            if image_width > image_height:
                new_width = max_size
                new_height = int((image_height / image_width) * max_size)
            else:
                new_width = int((image_width / image_height) * max_size)
                new_height = max_size

            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            center_x = (qr_img.size[0] - resized_image.size[0]) // 2
            center_y = (qr_img.size[1] - resized_image.size[1]) // 2

            #creating the qr code
            qr_img.paste(resized_image, (center_x, center_y))

            image_name = f"{''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))}.png"
            qr_path = os.path.join(settings.BASE_DIR, 'media/wifi_qr_codes/', image_name)        
            qr_img.save(qr_path)
           
            # qr_image_url = f"{settings.BASE_DIR}/media/wifi_qr_codes/{image_name}"
            # print(qr_image_url)

            event_res = create_event()
            event_id = event_res['event_id']

            save_url = "http://100002.pythonanywhere.com/"
            payload = {
                "cluster": "qr",
                "database": "qrcode",
                "collection": "wifi_qrcode",
                "document": "wifi_qrcode",
                "team_member_ID": "1146",
                "function_ID": "ABCDE",
                "command": "insert",
                "field": {
                    "wifi_ssid": wifi_name,
                    "wifi_password": wifi_password,
                    "function": "function",
                    "wifi_qr_url": qr_path,
                    "wifi_qr_image": qr_path,
                    "date" : date,
                    "time" : time,
                    "eventId": event_id,
                    "name": "",
                    "email": "",
                    "subject": "",
                    "content": ""
                },
                "update_field": {
                },
                "platform": "bangalore"
            }
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            res = requests.post(save_url, headers=headers, json=payload)

            #create new user for QR Code
            user_res = requests.get("https://100014.pythonanywhere.com/api/createuser/", headers=headers).json()

            returned_data = {
                'qrcode_image': qr_path,
                'username': user_res["username"],
                'password': user_res["password"],
                'role_id':res.json()['inserted_id']

            }

            return Response({"success": True, 'returned_data': returned_data, },status=HTTP_200_OK)
        except Exception as e:
            return Response(
                {"message": str(e), "success": False}, status=HTTP_400_BAD_REQUEST)
        
