# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from AMS.models import Student


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def SEND_SMS():
    account_sid = 'ACa1d79f7b530e58cbfdb3111f02a4eea6'
    auth_token =  '8b00647f4969217a01d55d073b502e1d'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="The Attendance has been taking successfully",
                        from_='+15075194764',
                        to='+918080004177'
                    )
    print("message sent sucessfully") 