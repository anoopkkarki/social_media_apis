#this program gets you the expiry date of the app token
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
# Replace with your own values

user_access_token = os.getenv('ACCESS_TOKEN')
app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')

def check_token_validity(user_access_token, app_id, app_secret):
    # Generate the App Access Token (app_id|app_secret)
    app_access_token = f'{app_id}|{app_secret}'
    
    # Facebook Debug Token API URL
    url = 'https://graph.facebook.com/debug_token'
    
    # Parameters to pass
    params = {
        'input_token': user_access_token,
        'access_token': app_access_token
    }
    
    # Make the API request to check token validity
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Check if the token is valid and get its expiration details
        if data.get('data', {}).get('is_valid'):
            expires_at = data['data'].get('expires_at')
            access_token = data['data'].get('access_token')
            if expires_at:
                expires_in = expires_at - int(time.time())
                print(f"Token expires in {expires_in} seconds.")
                print(type(expires_in))
                print(type(access_token))
                #print(data)
                
            else:
                print("No expiration information available.")
        else:
            print("Token is invalid.")
            print(data)
    else:
        print("Error with the request.")



# Run the check
if __name__ == "__main__":
    ex_user_access_token = "EAASVHp3KVqIBO7rm0RE6q65jKkiOazMZBmB2RZAQ2MOWJp8reN4svTslrLaBqcU72ip0yeUq5TZCb0BS9zJSZB3ODWAOM5pZBX0PA8XgFYjX3meoBgmUYGNm3oHlroaRxe0hzy7Gty3gpUvCsqSCQ67zZBuSn6yFChB0ZBQYgxRVQv0suQ7lC1USReLfPtgUnnUMGEDf23YGGEEu72X9QZDZD"
    user_access_token1 = "EAASVHp3KVqIBO4MsVQeZBSoZCWX2cAGL5ZA8NDZBFJdYV1ZA1P4ULlyZBVGvVYMZCQ4am3wNpZAEvU0ItcML5THg13XNitg20v3REAEAjIQLztZCw8QnN6mkaLHtoIembAx1RcQB6YpjabZBdIZA2kz5jUDm6dkvL0tRD1ZBslzZAUxMe5RWTfOQAVlhookvrzkLHdMTwp5ZBrfc2PFnGcagrlbwZDZD"
    user_access_token = "EAASVHp3KVqIBO2hZBh1Vw9wXIwfqhiWdfmrKoTy8pZCCAaNnJYiYbTdGgILoqXFnbUOLSLAdy6Nm5ZBsPSqO3cAkYqA5lxwlYqmoAPzz43Ef8wfV5vNp7l6lM5atFNmm2JmIVIKZAKtl59OvFBJh5cfCRuZBVvjnFpaeeJWPw49enlC86WI6baY9K3iK1TbV7PbqULDlLOcuDtaR2ZCKo73jyZBBlIZD"
    check_token_validity(user_access_token, app_id, app_secret)

