# IoT Lab 2 — Accessing IoT Devices via an Android Application

## Overview
This lab continues from IoT Lab 1. It introduces how to access and control IoT devices remotely using an Android app connected to a Raspberry Pi IoT gateway.  
The goal is to **view sensor values (e.g., temperature)** and **control actuators (e.g., lights)** from the Android app using SSH commands.

## Requirements
- Raspberry Pi 4 with network and SSH access  
- Temperature and humidity sensors connected through Telldus Live API  
- At least one actuator (e.g., lamp)  
- Android Studio installed on your computer  
- Internet connection  
- Emulator or physical Android device for testing

## Raspberry Pi Setup

### 1. Prepare the Pi and Scripts
Connect to your Raspberry Pi through SSH (you can use a terminal or PuTTY).  
Create four scripts in your home directory:
```
listdevices.py
listsensorsandvalues.py
turnondevice.py
turnoffdevice.py
```
Use `nano` or another text editor to paste the code provided in iLearn.  
Each script must include authentication fields (public and private keys, token, secret) provided during the lab.

### 2. Get the Actuator ID
Run:
```bash
python listdevices.py
```
Note the **ID** of your actuator and insert it into `turnondevice.py` and `turnoffdevice.py`.

### 3. Simplify Sensor Output
Modify `listsensorsandvalues.py` to print **only** the temperature value from the JSON response.  
Use:
```python
print(responseData['sensor'][0]['temp'])
```
This keeps the output easy to process from your Android app.

## Android App Setup

### 1. Create a New Android Project
In Android Studio:  
- New Project → **Empty Views Activity**  
- Language: **Java**  
- Project name: **IoTLab2App**  
- Wait until the project is built.

### 2. Edit Layout Files
In `app/src/main/res/layout/activity_main.xml`, define a simple interface that includes:  
- A `TextView` for showing temperature  
- A `Switch` to toggle the actuator  
- A `Button` to refresh data  

You can also use the provided `content_main.xml` layout from iLearn and replace your current layout content.

### 3. Update Resource Files
In `res/values/strings.xml`, add:
```xml
<string name="txv_title_temp">Smart Home</string>
<string name="txv_indoor_temp">Indoor temperature:</string>
<string name="txv_indoor_temp_show">11.11</string>
<string name="txv_outdoor_light">Lighting:</string>
<string name="txv_outdoor_light_show">Off</string>
<string name="txv_outdoor_light_on">On</string>
```
In `res/values/colors.xml`, add:
```xml
<color name="black_alpha">#000000</color>
<color name="text_box_background">#E7E7E7</color>
<color name="blue_text">#0166ff</color>
<color name="title_bar_color">#EB164E</color>
<color name="activitybackground">#ccf0f0</color>
<color name="activityfont">#3f3f3f</color>
```

### 4. Connect Layout and Logic
In `MainActivity.java`:
- Initialize UI elements with `findViewById()`  
- Add listeners to the toggle switch and button  
- Display the fetched temperature on the screen

Example:
```java
TextView txv_temp_indoor;
txv_temp_indoor = findViewById(R.id.indoorTempShow);
txv_temp_indoor.setText("Fetched temperature value");
```

### 5. Add SSH Support (via Ganymed SSH Library)
1. Download the **Ganymed SSH-2** `.jar` library.  
2. In Android Studio, create a folder `app/libs/` and copy the file `ssh.jar` inside.  
3. In `app/build.gradle.kts`, add:
```kotlin
implementation(files("libs/ssh.jar"))
```
4. Sync the project.

### 6. Implement SSH Connection
In `MainActivity.java`, create a `run(String command)` method that connects via SSH and executes a command.  
Use placeholder values for hostname, username, and password. Example:
```java
public void run(String command) {
    String hostname = "hostname";
    String username = "username";
    String password = "password";
    try {
        Connection conn = new Connection(hostname);
        conn.connect();
        boolean isAuthenticated = conn.authenticateWithPassword(username, password);
        if (!isAuthenticated) throw new IOException("Authentication failed.");
        Session sess = conn.openSession();
        sess.execCommand(command);
        BufferedReader br = new BufferedReader(new InputStreamReader(new StreamGobbler(sess.getStdout())));
        String line;
        while ((line = br.readLine()) != null) {
            System.out.println(line);
        }
        sess.close();
        conn.close();
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

### 7. Allow Internet Access
In `AndroidManifest.xml`, before `<application>`, add:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### 8. Use AsyncTask for Background Operations
To avoid blocking the UI when connecting via SSH, use `AsyncTask`. Example:
```java
new AsyncTask<Void, Void, Void>() {
    @Override
    protected Void doInBackground(Void... params) {
        run("python listsensorsandvalues.py");
        return null;
    }
    @Override
    protected void onPostExecute(Void v) {
        // Update TextView with fetched value
    }
}.execute();
```

## Expected Results
- The app displays the temperature value fetched from the Raspberry Pi.  
- The switch can turn the actuator (lamp) on and off remotely.  
- The “Update Temperature” button refreshes the temperature value in real-time.

## Troubleshooting
| Problem | Solution |
|----------|-----------|
| SSH authentication fails | Verify hostname and credentials with the lab instructor |
| App does not update value | Check AsyncTask and ensure `onPostExecute` updates the UI |
| Internet permission error | Confirm `<uses-permission>` is before `<application>` |
| Sensor value not found | Modify `listsensorsandvalues.py` to print only the temperature |

