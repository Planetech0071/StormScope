# StormScope

StormScope is a real-time lightning strike monitoring system that uses a Python client to listen for lightning strike data, calculates the distance to a user-defined location, and notifies a Google Apps Script web service when a strike occurs within a specified radius.

## Features

- **Real-time Lightning Detection:** Connects to the Blitzortung WebSocket API to receive live lightning strike data.
- **Location Tracking:** Periodically fetches the latest user location from a Google Apps Script endpoint.
- **Proximity Alerts:** Calculates the distance between the user's location and detected strikes using the Haversine formula.
- **Notification System:** Sends a notification to a Google Apps Script endpoint when a strike is detected within 5 km of the user's location, sending a notification to the client's phone.
- **Google Apps Script Integration:** Stores and retrieves location and strike data using two separate Apps Script web apps.

## File Overview

- [`main.py`](main.py):  
  The main Python client. Handles WebSocket communication, location updates, distance calculations, and notifications.

- [`APPS_SCRIPT_URL.gs`](APPS_SCRIPT_URL.gs):  
  Google Apps Script for storing and retrieving the latest user location (`lat`, `lon`, `timestamp`).  
  - `doPost`: Updates the stored location.
  - `doGet`: Returns the latest location as JSON.
  - Also found in: 'https://script.google.com/macros/s/AKfycbxLOtjk_znlYjxZFNIGfslz2UO5c3yYgSb2dWVpnHWBUd3UAc3zJhyCTqUrb1pHqGPH/exec'

- [`NOTIFY_SCRIPT_URL.gs`](NOTIFY_SCRIPT_URL.gs):  
  Google Apps Script for storing and retrieving the latest lightning strike notification.  
  - `doPost`: Stores strike information.
  - `doGet`: Returns the latest strike info as JSON. Supports clearing the stored strike with `?clear=1`.
  - Also found in: 'https://script.google.com/macros/s/AKfycbxKt0KiZWoxk6s3_CRhQpJHSaMu6I9FNXUsa1oKpP6grh5p1RVpaHhqFN-4BO5VKpMU/exec'

- [`README.md`](README.md):  
  Project documentation.

## How It Works

1. **Location Update:**  
   The iPhone updates its lastest Latitude and Longitude and POSTs it to the Apps Script Endpoint every 30 seconds. 
   The Python client fetches the latest location from the Apps Script endpoint every 30 seconds.

2. **Listening for Strikes:**  
   The client connects to the Blitzortung WebSocket API and listens for lightning strike messages.

3. **Distance Calculation:**  
   For each strike, the client extracts latitude and longitude, then calculates the distance to the user's current location.

4. **Notification:**  
   If a strike is within 5 km, the client sends a notification (with strike location, distance, and timestamp) to the notification Apps Script endpoint.

## Setup & Usage

### Prerequisites

- Python 3.7+
- `requests`, `websockets` libraries

Install dependencies:
```sh
pip install requests websockets
```

Install the iPhone shortcut:
- Find it here: 'https://www.icloud.com/shortcuts/551e8d410fff4227a68c5ad7513f8097'

### Configuration

1. **Deploy Google Apps Scripts:**
   - Deploy the code in [`APPS_SCRIPT_URL.gs`](APPS_SCRIPT_URL.gs) and [`NOTIFY_SCRIPT_URL.gs`](NOTIFY_SCRIPT_URL.gs) as separate web apps. (Or use mine [see above])
   - Update the `APPS_SCRIPT_URL` and `NOTIFY_SCRIPT_URL` variables in [`main.py`](main.py) with your deployed script URLs. (If you are not using my URLs)

2. **Run the Python Client:**
   ```sh
   python main.py
   ```

   The client will print "Online" and begin monitoring!

3. **Start the iPhone Shortcut:**
   - Start the iPhone shortcut by pressing the play (▶️) button and let it run in the background!
   - To stop it, press the stop (⏹️) button.

### License
- MIT License

----------------

## Note:
- This project is for educational and demonstration purposes. The Blitzortung WebSocket API is used here for real-time lightning data around the world; please respect their terms of use.