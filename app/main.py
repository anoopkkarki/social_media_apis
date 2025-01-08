import os
import requests

ACCESS_Token = os.get("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
API_URL=f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"

def post_to_facebook(message):
    payload = {
        "message":message,
        "access_token":ACCESS_Token,
    }
    response = request.post(API_URL,data=payload)
    if response.status_code == 200:
        print("post successfull :",response.json())
    else:
        print("error :",response.json())

if __name__ == "__main__":
    post_to_facebook("Hello, world!")


