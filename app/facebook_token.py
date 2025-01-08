import requests
from dotenv import load_dotenv
import os

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
    response = requests.get(url,params=params)

    if response.status_code == 200:
        long_lived_token = response.json().get('access_token')
        expiry = response.json().get('expires_in')
        print(f"Long-lived Token: {long_lived_token}")
        print(f"Expires in: {expiry} seconds")
        return long_lived_token
    else:
        print(f"Error: {response.json()}")
        return None

# Call the function to get the long-lived token
long_lived_token = get_long_lived_token()
