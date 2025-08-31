import re
import asyncio
import websockets
import requests
import math
import threading
import time

def extract_lat_lon(msg):
	lat_match = re.search(r'lat[\.:]?([\d\-\.]+)', msg)
	lon_match = re.search(r'lon[\.:]?([\d\-\.]+)', msg)
	if lat_match and lon_match:
		try:
			lat = float(lat_match.group(1))
			lon = float(lon_match.group(1))
			return lat, lon
		except Exception:
			return None
	return None

# Haversine formula to calculate distance between two lat/lon points in km
def haversine(lat1, lon1, lat2, lon2):
	R = 6371  # Earth radius in km
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	dphi = math.radians(lat2 - lat1)
	dlambda = math.radians(lon2 - lon1)
	a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	return R * c


# Set your Google Apps Script web app URL here:
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxLOtjk_znlYjxZFNIGfslz2UO5c3yYgSb2dWVpnHWBUd3UAc3zJhyCTqUrb1pHqGPH/exec"

# Shared variable for latest location
latest_location = {'lat': 29.0847, 'lon': -80.9983}

def fetch_latest_location():
	global latest_location
	try:
		resp = requests.get(APPS_SCRIPT_URL)
		if resp.status_code == 200:
			data = resp.json()
			lat = float(data.get('lat', 29.0847))
			lon = float(data.get('lon', -80.9983))
			latest_location['lat'] = lat
			latest_location['lon'] = lon
		else:
			print(f"Failed to fetch location: {resp.status_code} {resp.text}")
	except Exception as e:
		print(f"Error fetching location: {e}")
def location_updater():
	while True:
		fetch_latest_location()
		time.sleep(30)


NOTIFY_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxKt0KiZWoxk6s3_CRhQpJHSaMu6I9FNXUsa1oKpP6grh5p1RVpaHhqFN-4BO5VKpMU/exec"

def notify_strike(lat, lon, dist):
	dist = round(dist, 2)  # Round distance to 2 decimal places
	data = {
		"lat": lat,
		"lon": lon,
		"dist": dist,
		"timestamp": time.time()
	}
	try:
		resp = requests.post(NOTIFY_SCRIPT_URL, json=data)
	except Exception as e:
		print(f"Failed to post to Apps Script: {e}")

async def ws_client():
	uri = "wss://ws1.blitzortung.org/"
	async with websockets.connect(uri) as websocket:
		await websocket.send('{"a":111}')
		try:
			async for message in websocket:
				decoded = re.sub(r'[^\x00-\x7F]+', '', message)
				latlon = extract_lat_lon(decoded)
				if latlon:
					strike_lat, strike_lon = latlon
					user_lat = latest_location['lat']
					user_lon = latest_location['lon']
					dist = haversine(user_lat, user_lon, strike_lat, strike_lon)
					if dist <= 5:
						notify_strike(strike_lat, strike_lon, dist)
		except websockets.ConnectionClosed:
			print("WebSocket connection closed.")

if __name__ == "__main__":
	print("Online")
	# Start location updater thread
	updater_thread = threading.Thread(target=location_updater, daemon=True)
	updater_thread.start()
	asyncio.run(ws_client())
