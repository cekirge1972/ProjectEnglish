import requests
import json
from datetime import datetime

def add_exceptional_time(base_url, app_name, duration_seconds, exception_date=None):
    """
    Sends a POST request to the Secondary API to add an exception for a specific app.
    
    :param base_url: The URL of the Secondary API (e.g., 'http://YOUR_SERVER_IP:5001')
    :param app_name: Name of the executable (e.g., 'discord.exe')
    :param duration_seconds: Extra time allowed in seconds
    :param exception_date: Date string (YYYY-MM-DD). Defaults to today.
    :return: Response dictionary from the API
    """
    
    # Default to today's date if not provided
    if not exception_date:
        exception_date = datetime.now().strftime('%Y-%m-%d')
    
    endpoint = f"{base_url}/api/exceptions"
    
    # Construct the payload based on your API documentation
    payload = {
        "app_name": app_name,
        "date": exception_date,
        "extra_time": duration_seconds
    }
    
    try:
        response = requests.post(
            endpoint, 
            json=payload, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        
        # Parse the JSON response
        result = response.json()
        
        if response.status_code == 200 or response.status_code == 201:
            if result.get("status") == "queued":
                return (f"⚠️ [Queued] Primary API offline. Request for {app_name} saved to buffer.")
            else:
                return (f"✅ [Success] Exception added for {app_name} on {exception_date}.")
            """ return result """
        else:
            return (f"❌ [Error] Server returned status {response.status_code}: {response.text}")
            """ return None """

    except requests.exceptions.RequestException as e:
        print(f"🚨 [Connection Error] Could not reach the Secondary API: {e}")
        return None

# --- Example Usage ---
# API_URL = "http://192.168.1.50:5001"
# add_exceptional_time(API_URL, "chrome.exe", 3600) # Adds 1 hour for today