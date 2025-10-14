# IoT Lab 1 – Telldus API Control via Raspberry Pi

This guide explains how to connect to your Raspberry Pi via SSH, set up the IoT Lab 1 folder, copy all files, update your Telldus API keys, and run both the **original** and **enhanced** versions of the Python scripts.

---

## 1. Connect to the Raspberry Pi via SSH

1. Make sure your Raspberry Pi is online and reachable inside the lab network.
2. From your local terminal, connect using the provided hostname (replace `<username>` and `<rpi-name>` if necessary):

```bash
ssh <username>@<rpi-name>.dsv.su.se
```

**Example:**

```bash
ssh student@rpi-v5-12.dsv.su.se
```

If prompted to confirm the connection, type **yes** and enter your password.

---

## 2. Create the IoT Lab Folder

Once you are connected to the Raspberry Pi, create the project folders:

```bash
mkdir -p ~/IoTLab1/original
mkdir -p ~/IoTLab1/enhanced
```

---

## 3. Copy the Files from Your Local Computer

From your local computer, open a terminal in the folder containing the project and copy all files to your Raspberry Pi using **scp**:

```bash
scp -r IoTLab1/ <username>@<rpi-name>.dsv.su.se:~/
```

**Example:**

```bash
scp -r IoTLab1/ student@rpi-v5-12.dsv.su.se:~/
```

This command transfers the full folder (with both `original` and `enhanced` subfolders) into your Raspberry Pi home directory.

---

## 4. Update Your Telldus API Keys

You need your personal API keys from the Telldus developer portal:

👉 [https://api.telldus.com/keys](https://api.telldus.com/keys)

### For **Original Scripts**

Each original file contains this section at the top:

```python
pubkey = "YOUR_PUBLIC_KEY"
privkey = "YOUR_PRIVATE_KEY"
token  = "YOUR_TOKEN"
secret = "YOUR_TOKEN_SECRET"
```

Replace these placeholder values with your actual Telldus API credentials.

You can edit directly on the Raspberry Pi with:

```bash
nano ~/IoTLab1/original/ListDevices.py
```

Repeat for each file in the `original` folder.

---

### For **Enhanced Scripts**

All enhanced scripts load the keys automatically from a single file:

```bash
~/IoTLab1/enhanced/credentials.py
```

Edit this file once with your real keys:

```bash
nano ~/IoTLab1/enhanced/credentials.py
```

It should look like this after editing:

```python
pubkey = "YOUR_REAL_PUBLIC_KEY"
privkey = "YOUR_REAL_PRIVATE_KEY"
token  = "YOUR_REAL_TOKEN"
secret = "YOUR_REAL_TOKEN_SECRET"
```

Press **Ctrl + O** to save, then **Ctrl + X** to exit.

---

## 5. Check Python Installation

Make sure Python 3 is available on the Raspberry Pi:

```bash
python3 --version
```

If it’s installed, you can proceed to run the scripts.

---

## 6. Run the Original Scripts

### List Sensors
```bash
python3 ~/IoTLab1/original/ListSensors.py
```

### List Devices
```bash
python3 ~/IoTLab1/original/ListDevices.py
```

### Turn ON a Device

1. Open `TurnOn.py` and replace the placeholder:
   ```python
   DEVICE_ID = "PUT_DEVICE_ID_HERE"
   ```
2. Run:
   ```bash
   python3 ~/IoTLab1/original/TurnOn.py
   ```

### Turn OFF a Device

1. Open `TurnOff.py` and replace:
   ```python
   DEVICE_ID = "PUT_DEVICE_ID_HERE"
   ```
2. Run:
   ```bash
   python3 ~/IoTLab1/original/TurnOff.py
   ```

---

## 7. Run the Enhanced Scripts

The enhanced versions do not require editing the code each time.
They use the keys from `credentials.py` and can be executed directly by **device name**.

### List Sensors
```bash
python3 ~/IoTLab1/enhanced/ListSensors.py
```

### List Devices
```bash
python3 ~/IoTLab1/enhanced/ListDevices.py
```

### Turn ON a Device by Name
```bash
python3 ~/IoTLab1/enhanced/TurnOn.py "device-name"
```

### Turn OFF a Device by Name
```bash
python3 ~/IoTLab1/enhanced/TurnOff.py "device-name"
```

**Example:**

```bash
python3 ~/IoTLab1/enhanced/TurnOn.py "tempsensor20-ch7"
python3 ~/IoTLab1/enhanced/TurnOff.py "tempsensor20-ch7"
```

---

## 8. Optional – Run Sequential Test (List → ON → OFF)

If you want to quickly test all steps together, you can run:

```bash
cd ~/IoTLab1/enhanced
python3 ListDevices.py
python3 TurnOn.py "tempsensor20-ch7"
sleep 3
python3 TurnOff.py "tempsensor20-ch7"
```

---

## 9. Troubleshooting

| Problem | Possible Cause | Solution |
|----------|----------------|-----------|
| `Device not found` | Wrong name or spacing | Run `ListDevices.py` to check the exact name |
| `401 Unauthorized` | Wrong or expired API keys | Re-check your credentials in `credentials.py` |
| `Timeout` | Network connection issue | Verify Raspberry Pi is connected to the lab Wi-Fi |
| Script hangs | Unresponsive device | Press **Ctrl + C** to stop the script |

---

## 10. Folder Structure Overview

```
IoTLab1/
├── original/
│   ├── ListDevices.py
│   ├── ListSensors.py
│   ├── TurnOn.py
│   └── TurnOff.py
│
├── enhanced/
│   ├── credentials.py
│   ├── ListDevices.py
│   ├── ListSensors.py
│   ├── TurnOn.py
│   └── TurnOff.py
│
└── README.md
```

---

## 11. Quick Recap

| Task | Original Script | Enhanced Script |
|------|-----------------|----------------|
| List Sensors | `ListSensors.py` | `ListSensors.py` |
| List Devices | `ListDevices.py` | `ListDevices.py` |
| Turn ON | `TurnOn.py` (edit ID) | `TurnOn.py "device-name"` |
| Turn OFF | `TurnOff.py` (edit ID) | `TurnOff.py "device-name"` |
| API Keys | In every file | In `credentials.py` |

---

## You are ready!

Your Raspberry Pi is now configured to communicate with the Telldus API.
You can list devices, monitor sensors, and control IoT components directly through Python scripts.