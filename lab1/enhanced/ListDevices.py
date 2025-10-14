# IoTLab1/enhanced/ListDevices.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, json, uuid, time, requests
from credentials import pubkey, privkey, token, secret

def oauth_header():
    timestamp  = str(int(time.time()))
    nonce      = uuid.uuid4().hex
    signature  = privkey + "%26" + secret
    return {
        "Authorization": 'OAuth oauth_consumer_key="{k}", '
                         'oauth_nonce="{n}", '
                         'oauth_signature="{s}", '
                         'oauth_signature_method="PLAINTEXT", '
                         'oauth_timestamp="{t}", '
                         'oauth_token="{tok}", '
                         'oauth_version="1.0"'.format(
                             k=pubkey, n=nonce, s=signature, t=timestamp, tok=token
                         )
    }

def main():
    try:
        r = requests.get(
            "https://pa-api.telldus.com/json/devices/list",
            headers=oauth_header(),
            timeout=20,
        )
        r.raise_for_status()
        print(json.dumps(r.json(), indent=2, sort_keys=True))
    except Exception as e:
        print("Error listing devices:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
