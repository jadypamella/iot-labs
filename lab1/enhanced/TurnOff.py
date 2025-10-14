# IoTLab1/enhanced/TurnOff.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Turns off a device by its NAME.
Usage:
  python TurnOff.py "device-name"
"""

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

def find_device_id_by_name(name):
    r = requests.get(
        "https://pa-api.telldus.com/json/devices/list",
        headers=oauth_header(),
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    devices = data.get("device", []) or []

    exact = [d for d in devices if d.get("name") == name]
    if len(exact) >= 1:
        return exact[0].get("id")

    partial = [d for d in devices if name.lower() in str(d.get("name","")).lower()]
    if len(partial) == 1:
        return partial[0].get("id")

    if len(partial) > 1:
        print("Multiple devices matched:")
        for d in partial:
            print("  id:", d.get("id"), "name:", d.get("name"))
        return None

    return None

def main():
    if len(sys.argv) < 2:
        print('Usage: python TurnOff.py "device-name"')
        sys.exit(2)
    name = sys.argv[1]

    try:
        dev_id = find_device_id_by_name(name)
        if not dev_id:
            print("Device not found:", name)
            sys.exit(3)

        r = requests.get(
            "https://pa-api.telldus.com/json/device/turnOff",
            params={"id": str(dev_id)},
            headers=oauth_header(),
            timeout=20,
        )
        r.raise_for_status()
        print(json.dumps(r.json(), indent=2, sort_keys=True))
    except Exception as e:
        print("Error turning off device:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
