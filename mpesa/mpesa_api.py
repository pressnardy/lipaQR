import requests
from mpesa import mpesa_settings

STK_REQUEST_BODY = mpesa_settings.STK_REQUEST_BODY
HEADERS = mpesa_settings.HEADERS
URL = mpesa_settings.MPESA_STK_PUSH_URL


def send_stk_push(phone_number, amount, account_reference):
    STK_REQUEST_BODY['PartyA'] = str(phone_number)
    STK_REQUEST_BODY['Amount'] = str(amount)
    STK_REQUEST_BODY['PhoneNumber'] = str(phone_number)
    STK_REQUEST_BODY['AccountReference'] = str(account_reference)

    try:
        response = requests.post(url=URL, json=STK_REQUEST_BODY, headers=HEADERS).json()

    except Exception as e:
        raise ValueError(f"STK Push error as: {e}")
    return response


if __name__ == "__main__":
    print(send_stk_push('254706088217', '10', '254706088217'))

