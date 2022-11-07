
from base64 import b64decode
from json import loads, dumps
import random, string, uuid, requests

# Session barer token (you should have it after login)
session_header = "eyJraWQiOiIxIiwiYWxnIjoiSFMyNTY..."
# Your device id (you can generate it but be sure to use the same id from login to checkout)
device_id = "C665AA42-43E6-4203-AA92-4EB78F21BC11" 
# Solve reCaptcha (sitekey: 6LcuURUTAAAAAK_b8wWvbNLY0awdFT27EJYcx-M1, url: https://ms-api.sivasdescalzo.com)
captcha = "03AIIuk..."


# <==============> Generate Auth Fingerprint <==============> #

url = "https://ms-api.sivasdescalzo.com/api/carts/payments/token"
querystring = {"isRaffleParticipation":"true"} 
headers = {
    "cookie": "country=IT",
    "Host": "ms-api.sivasdescalzo.com",
    "Pragma": "no-cache",
    "Accept": "application/json",
    "Device-Os": "I-iOS 12.1.2",
    "Authorization": f"Bearer {session_header}",
    "App-Version": "2.4.1",
    "Device-Id": device_id,
    "X-Recaptcha": captcha,
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-us",
    "Cache-Control": "no-cache",
    "Store-Code": "it",
    "User-Agent": "SVD/2002252238 CFNetwork/976 Darwin/18.2.0",
    "Bundle-Version": "53",
    "Cookie": "country=IT"
}

response = requests.request("GET", url, headers=headers, params=querystring)

params = {
    "token": response.json()["token"],
    "device_id": device_id
}

# <==============> Generate PayPal url <==============> #

data = loads(b64decode(params['token'].encode())) 
url = "https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/paypal_hermes/setup_billing_agreement"
payload = {
    "experience_profile": {
        "brand_name": "SVD - sivasdescalzo",
        "no_shipping": 1,
        "address_override": False
    },
    "authorization_fingerprint": data["authorizationFingerprint"],
    "offer_pay_later": False,
    "cancel_url": "com.sivasdescalzo.svd-app.payments://onetouch/v1/cancel",
    "return_url": "com.sivasdescalzo.svd-app.payments://onetouch/v1/success",
    "offer_paypal_credit": False,
    "_meta": {
        "iosIdentifierForVendor": params["device_id"],
        "source": "paypal-browser",
        "iosDeviceName": "iPhone",
        "merchantAppName": "SVD",
        "integration": "dropin2",
        "deviceAppGeneratedPersistentUuid": str(uuid.uuid4()).upper(),
        "merchantAppVersion": "2002252238",
        "iosIsCocoapods": True,
        "sessionId": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32)),
        "iosSystemName": "iOS",
        "merchantAppId": "com.sivasdescalzo.svd-app",
        "platform": "iOS",
        "isSimulator": False,
        "iosDeploymentTarget": "120000",
        "sdkVersion": "4.38.0",
        "deviceManufacturer": "Apple",
        "deviceModel": "iPhone9,4",
        "deviceScreenOrientation": "Portrait",
        "venmoInstalled": False,
        "dropinVersion": "8.2.0",
        "iosBaseSDK": "150200",
        "platformVersion": "12.1.2"
    }
}
headers = {
    "Host": "api.braintreegateway.com:443",
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Braintree/iOS/4.38.0",
    "Accept-Language": "en-IT",
    "Content-Length": "1665",
    "Connection": "close"
} 
response = requests.request("POST", url, json=payload, headers=headers) 
token = response.json()['agreementSetup']['tokenId'] 
# <==============> Generate PayPal url <==============> 

# Actually pay the link
...



# <==============>   Final Post   <==============> 

data = {
	"_meta": payload['_meta'],
	"authorization_fingerprint": payload['authorization_fingerprint'],
	"paypal_account": {
		"correlation_id": token,
		"response": {
			"webURL": f"com.sivasdescalzo.svd-app.payments:\/\/onetouch\/v1\/success?token={token}&ba_token=BA-7PR86517AU142474L"
		},
		"client": {
			"environment": "live",
			"product_name": "PayPalSDK\/OneTouchCore-iOS 4.38.0 (iPhone (iPhone9,4); iPhone9,4; RELEASE)",
			"paypal_sdk_version": "4.38.0",
			"platform": "iOS"
		},
		"response_type": "web"
	}
}
url = "https://api.braintreegateway.com/merchants/7rgb8j8vb5f4hdwg/client_api/v1/payment_methods/paypal_accounts"

headers = {
    'Host': "api.braintreegateway.com:443",
    'Accept': "application/json",
    'Content-Type': "application/json; charset=utf-8",
    'Accept-Encoding': "gzip, deflate",
    'User-Agent': "Braintree/iOS/4.38.0",
    'Accept-Language': "en-IT", 
    'Connection': "close"
}
response = requests.request("POST", url, json=data, headers=headers) 

''' RESPONSE

{
    "paypalAccounts": [
        {
            "type": "PayPalAccount",
            "nonce": "cfcc7ad3-7632-1e7c-ca96-a8ab385c2429", # payment_data parameter
            "description": "PayPal",
            "consumed": false,
            "details": { # Paypal account details
                    "email": "xxx@protonmail.com",
                    "payerInfo": {
                    "shippingAddress": null,
                    "email": "xxx@protonmail.com",
                    "firstName": "xxx",
                    "lastName": "xxx",
                    "countryCode": "IT",
                    "payerId": "KBN34RPSJ97CQ",
                    "phone": "+44 3412735654",
                    "tenant": "PAYPAL"
                },
                "correlationId": "BA-7PR86517AU142474D", # Paypal token
                "billingAddress": null,
                "shippingAddress": null
            }
        }
    ]
}
'''