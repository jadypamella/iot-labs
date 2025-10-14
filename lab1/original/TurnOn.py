# IoTLab1/original/TurnOn.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Insert your generated API keys from http://api.telldus.com/keys
pubkey = "YOUR_PUBLIC_KEY"
privkey = "YOUR_PRIVATE_KEY"
token  = "YOUR_TOKEN"
secret = "YOUR_TOKEN_SECRET"

# Fill the placeholder below with the device id before running
DEVICE_ID = "PUT_DEVICE_ID_HERE"

import requests, json, uuid, time

localtime  = time.localtime(time.time())
timestamp  = str(int(time.mktime(localtime)))
nonce      = uuid.uuid4().hex
oauthSignature = privkey + "%26" + secret

response = requests.get(
    url="https://pa-api.telldus.com/json/device/turnOn",
    params={"id": DEVICE_ID},
    headers={
        "Authorization": 'OAuth oauth_consumer_key="{pubkey}", '
                         'oauth_nonce="{nonce}", '
                         'oauth_signature="{oauthSignature}", '
                         'oauth_signature_method="PLAINTEXT", '
                         'oauth_timestamp="{timestamp}", '
                         'oauth_token="{token}", '
                         'oauth_version="1.0"'.format(
                            pubkey=pubkey,
                            nonce=nonce,
                            oauthSignature=oauthSignature,
                            timestamp=timestamp,
                            token=token
                         )
    },
)

print(json.dumps(response.json(), indent=4, sort_keys=True))
