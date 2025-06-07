from datetime import datetime
import base64
import requests
import os
from dotenv import load_dotenv
load_dotenv()


MPESA_CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_BUSINESS_SHORTCODE = os.getenv('MPESA_BUSINESS_SHORTCODE')
MPESA_CREDENTIALS_URL =  os.getenv('MPESA_CREDENTIALS_URL')
MPESA_STK_PUSH_URL = os.getenv('MPESA_STK_PUSH_URL')
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')

TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
STK_PASSWORD = base64.b64encode((MPESA_BUSINESS_SHORTCODE + MPESA_PASSKEY + TIMESTAMP).encode()).decode()


def get_access_token():
    encoded_credentials = base64.b64encode(f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url=MPESA_CREDENTIALS_URL, headers=headers).json()
        return str(response["access_token"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e))


HEADERS = {
    'Authorization': 'Bearer ' + get_access_token(),
    'Content-Type': 'application/json'
}


STK_REQUEST_BODY = {
    "BusinessShortCode": MPESA_BUSINESS_SHORTCODE,
    "Password": STK_PASSWORD,
    "Timestamp": TIMESTAMP,
    "TransactionType": "CustomerPayBillOnline", #till "CustomerBuyGoodsOnline"
    "Amount": "10",
    "PartyA": "254708374149",
    "PartyB": MPESA_BUSINESS_SHORTCODE,
    "PhoneNumber": "254708374149",
    "CallBackURL": MPESA_CALLBACK_URL,
    "AccountReference": "account",
    "TransactionDesc": "test"
}


def send_stk_push():
    try:
        response = requests.post(url=MPESA_STK_PUSH_URL, json=STK_REQUEST_BODY, headers=HEADERS).json()
    except Exception as e:
        response = 'Error:', str(e)
    return response


if __name__ == "__main__":
    print(send_stk_push())

