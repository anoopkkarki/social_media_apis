import requests
from dotenv import load_dotenv
import os
import time

import  update_to_env as updateEnv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')
short_lived_token = os.getenv('ACCESS_TOKEN')

# Exchange short-lived token for long-lived token
def get_long_lived_token():
    url = f"https://graph.facebook.com/v21.0/oauth/access_token"
    params= {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }
    try:
        response = requests.get(url,params=params)
    
        if response.status_code == 200:
            long_lived_token = response.json().get('access_token')
            expiry = response.json().get('expires_in')
            expiry_timestamp = int(time.time()) + expiry  # Calculate the actual expiry timestamp
            print(f"Long-lived Token: {long_lived_token}")
            print(f"Expires in: {expiry} seconds")
            print(f"Expiry Timestamp: {expiry_timestamp}")
            return long_lived_token,expiry_timestamp
        else:
            print(f"Error: {response.json()}")
            return None,None
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None, None

def check_token_expiry():
    expiry_timestamp = os.getenv("fb_token_expiry")
    print(expiry_timestamp)
    print(f'short_lived_token = {short_lived_token}')
    current_time = int(time.time())  # Get current timestamp
    print(f"Current Time: {current_time}")
    if expiry_timestamp:
          expiry_timestamp = int(expiry_timestamp)  # Convert the expiry to an integer

    else:
        print("Facebook access_token expiry not found ...calling token value extraction function")
        long_lived_token,expiry_timestamp = get_long_lived_token()
        if long_lived_token and expiry_timestamp:
            updateEnv.update_env_file("fb_token_expiry",expiry_timestamp)
            updateEnv.update_env_file("ACCESS_TOKEN",long_lived_token)
        else:
            print("Error: Could not fetch long-lived token and expiry.")
            return

    # Check if expiry is less than 3 days (259200 seconds)
    if expiry_timestamp - current_time <= 259200:
        print("Token is about to expire. fetching a new one .......")
        long_lived_token,expiry_timestamp = get_long_lived_token()
        if long_lived_token:
            updateEnv.update_env_file("fb_token_expiry",expiry_timestamp)
            updateEnv.update_env_file("ACCESS_TOKEN", long_lived_token)
        else:
            print("Error: Could not fetch new token.")
    else:
        print("current token is still valid")


# Call the function to get the long-lived token
if __name__ == "__main__":
    #long_lived_token,expiry = get_long_lived_token()
    check_token_expiry()
