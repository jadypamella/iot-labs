# IoTLab1/enhanced/ListDevices.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Pretty prints devices in a clean table.
Optional name filter:
  python ListDevices.py
  python ListDevices.py lamp
"""

import sys
import json
import uuid
import time
import requests
from datetime import datetime, timezone
from credentials import pubkey, privkey, token, secret

API_URL = "https://pa-api.telldus.com/json/devices/list"

METHOD_FLAGS = {
    1:  "TURNON",
    2:  "TURNOFF",
    4:  "BELL",
    8:  "TOGGLE",
    16: "DIM",
    32: "LEARN",
    64: "EXECUTE",
    128:"UP",
    256:"DOWN",
    512:"STOP",
}

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

def human_time(ts):
    try:
        ts_int = int(ts)
        dt = datetime.fromtimestamp(ts_int, tz=timezone.utc)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return str(ts) if ts is not None else ""

def methods_label(mbits):
    try:
        val = int(mbits)
    except Exception:
        return ""
    names = [name for bit, name in METHOD_FLAGS.items() if val & bit]
    return ",".join(names) if names else str(val)

def collect_rows(data, name_filter=None):
    devices = data.get("device", []) or data.get("devices", []) or []
    rows = []
    for d in devices:
        name = d.get("name") or ""
        if name_filter and name_filter.lower() not in name.lower():
            continue
        row = {
            "Name": name or "(unnamed)",
            "Type": d.get("type", ""),
            "State": d.get("state", ""),
            "Value": d.get("statevalue", ""),
            "Methods": methods_label(d.get("methods")),
            "Client": d.get("clientName", d.get("client", "")),
            "Editable": str(d.get("editable", "")),
            "Updated": human_time(d.get("lastUpdated")),
            "Id": d.get("id", ""),
        }
        rows.append(row)
    rows.sort(key=lambda r: (r["Name"], str(r["Id"])))
    return rows

def calc_widths(rows, headers):
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(r.get(h, ""))))
    return widths

def print_table(rows):
    if not rows:
        print("No devices found")
        return
    headers = ["Name", "Type", "State", "Value", "Methods", "Client", "Editable", "Updated", "Id"]
    widths = calc_widths(rows, headers)

    def line(char="="):
        print(" ".join(char * widths[h] for h in headers))

    line("=")
    print(" ".join(h.ljust(widths[h]) for h in headers))
    line("=")

    for r in rows:
        print(" ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers))

    line("=")

def main():
    name_filter = sys.argv[1].strip() if len(sys.argv) > 1 else None
    try:
        r = requests.get(API_URL, headers=oauth_header(), timeout=20)
        r.raise_for_status()
        data = r.json()
        rows = collect_rows(data, name_filter=name_filter)
        print_table(rows)
    except requests.HTTPError as e:
        print("HTTP error:", e)
        try:
            print("Response:", r.text[:500])
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print("Error listing devices:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
