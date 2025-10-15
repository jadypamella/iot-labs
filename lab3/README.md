# IoT Lab 3 — Raspberry Pi + MQTT + Android App

## Overview
This lab connects sensors on a Raspberry Pi to an Android app using the MQTT protocol.  
The Raspberry Pi reads data from sensors and publishes messages to a public broker (`test.mosquitto.org`).  
The Android app subscribes to the same topic and displays live sensor values.

## Requirements
- Raspberry Pi 4 with Raspbian installed and SSH enabled  
- At least one Adafruit sensor (light, proximity, or color)  
- Android Studio (latest version)  
- Internet connection  
- Smartphone or emulator for testing

## Raspberry Pi Setup

### 1. Enable interfaces
```bash
sudo apt-get install -y python-smbus i2c-tools
sudo raspi-config
```
Then enable I2C and SPI under “Interfacing Options”.  
Reboot:
```bash
sudo reboot
```

### 2. Check sensor connection
After wiring the sensor (3.3V → Vin, GND → GND, GPIO2 → SDA, GPIO3 → SCL):
```bash
sudo i2cdetect -y 1
```
You should see a hex address (e.g. `29`, `39`, `57`).

### 3. Install Python libraries
```bash
pip3 install RPI.GPIO adafruit-blinka paho-mqtt
pip3 install adafruit-circuitpython-tsl2591
pip3 install adafruit-circuitpython-vcnl4010
pip3 install adafruit-circuitpython-tcs34725
```

### 4. Run the MQTT publisher
Download `mqtt-template-lab3.py` (from iLearn), edit it:
```python
broker = "test.mosquitto.org"
pub_topic = "iotlab/yourname/sensor"
```
Uncomment the sensor you are using, then run:
```bash
python3 mqtt-template-lab3.py
```

Your Pi now publishes sensor readings to the MQTT broker.

## Android App Setup (IoTLab3App)

### 1. Create a new project
In Android Studio → New Project → Empty Views Activity  
Language: Java  
Name: IoTLab3App

### 2. Required files to edit
| File | Path | Purpose |
|------|------|----------|
| `MainActivity.java` | `app/src/main/java/com/example/iotlab3app/` | Handles MQTT connection, subscription, and UI updates |
| `activity_main.xml` | `app/src/main/res/layout/` | Defines layout (TextViews + Button) |
| `AndroidManifest.xml` | `app/src/main/` | Adds Internet permissions and MQTT service |
| `build.gradle.kts` | `app/` | Adds MQTT library dependencies |
| `settings.gradle.kts` | Root | Adds Paho repository |
| `colors.xml` | `app/src/main/res/values/` | Color palette |

### 3. Add MQTT libraries
In `app/build.gradle.kts`:
```kotlin
dependencies {
    implementation("org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.1.0")
    implementation("org.eclipse.paho:org.eclipse.paho.android.service:1.1.1")
    implementation("androidx.legacy:legacy-support-v4:1.0.0")
}
```

In `settings.gradle.kts`:
```kotlin
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven { url = uri("https://repo.eclipse.org/content/repositories/paho-snapshots/") }
    }
}
```

### 4. Add permissions
In `AndroidManifest.xml`, outside `<application>`:
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
```
Inside `<application>`:
```xml
<service android:name="org.eclipse.paho.android.service.MqttService"/>
```

### 5. Set your MQTT topic
In `MainActivity.java`:
```java
private static final String TOPIC = "iotlab/yourname/sensor";
```
Make sure it’s the same as in your Raspberry Pi script.

### 6. Run the app
1. Connect your phone or use an emulator.  
2. Press Run ▶ in Android Studio.  
3. The app will connect to `test.mosquitto.org` and show messages received on your topic.  

If you send RGB values or lux readings, they will appear in the app instantly.

## Troubleshooting
| Issue | Fix |
|-------|-----|
| App shows nothing | Make sure Pi and app use the same topic |
| Connection error | Check Internet or firewall; test broker with MQTT Explorer |
| Permission denied | Ensure Internet permission is added before `<application>` |
| Sensor not found | Recheck wiring and run `sudo i2cdetect -y 1` again |
