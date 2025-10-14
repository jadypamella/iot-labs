# IoTLab1/enhanced/ListSensors.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Pretty prints sensors with key fields in a clean table.
Optional name filter:
  python ListSensors.py
  python ListSensors.py tempsensor20
"""

import sys
import json
import uuid
import time
import requests
from datetime import datetime, timezone
from credentials import pubkey, privkey, token, secret

API_URL = "https://pa-api.telldus.com/json/sensors/list"

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

def parse_misc_values(misc_values):
    """miscValues comes as '{}' or a JSON string like '{"chId": 151}'"""
    if not misc_values:
        return {}
    if isinstance(misc_values, dict):
        return misc_values
    try:
        return json.loads(misc_values)
    except Exception:
        return {}

def human_time(ts):
    """lastUpdated appears as unix seconds"""
    try:
        ts_int = int(ts)
        dt = datetime.fromtimestamp(ts_int, tz=timezone.utc)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return str(ts)

def battery_label(b):
    """Telldus often reports 254 for ok. Show raw and label."""
    try:
        val = int(b)
    except Exception:
        return str(b) if b is not None else ""
    if val == 254:
        return "OK (254)"
    return str(val)

def online_label(v):
    return "online" if str(v) == "1" else "offline"

def collect_rows(data, name_filter=None):
    sensors = data.get("sensor", []) or data.get("sensors", []) or []
    rows = []
    for s in sensors:
        name = s.get("name") or ""
        if name_filter and name_filter.lower() not in str(name).lower():
            continue
        misc = parse_misc_values(s.get("miscValues"))
        ch = misc.get("chId", "")
        row = {
            "Name": name or "(unnamed)",
            "Model": s.get("model", ""),
            "Temp°C": s.get("temp", ""),
            "Hum%": s.get("humidity", ""),
            "Status": online_label(s.get("online")),
            "Battery": battery_label(s.get("battery")),
            "Channel": ch,
            "Updated": human_time(s.get("lastUpdated")),
            "SensorId": s.get("sensorId", ""),
            "Id": s.get("id", ""),
        }
        rows.append(row)
    # sort by Name then SensorId for stable output
    rows.sort(key=lambda r: (r["Name"], str(r["SensorId"])))
    return rows

def calc_widths(rows, headers):
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(r.get(h, ""))))
    return widths

def print_table(rows):
    if not rows:
        print("No sensors found")
        return
    headers = ["Name", "Model", "Temp°C", "Hum%", "Status", "Battery", "Channel", "Updated", "SensorId", "Id"]
    widths = calc_widths(rows, headers)

    def line(char="="):
        print(" ".join(char * widths[h] for h in headers))

    # header
    line("=")
    print(" ".join(str(h).ljust(widths[h]) for h in headers))
    line("=")

    # rows
    for r in rows:
        print(" ".join(str(r.get(h, "")).ljust(widths[h]) for h in headers))

    line("=")

def main():
    # optional filter by substring of name
    name_filter = sys.argv[1].strip() if len(sys.argv) > 1 else None

    try:
        r = requests.get(
            API_URL,
            params={"includeValues": "1"},
            headers=oauth_header(),
            timeout=20,
        )
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
        print("Error listing sensors:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
