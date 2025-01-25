import requests
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
INSTAGRAM_ACCOUNT_ID=os.getenv('INSTAGRAM_ACCOUNT_ID')



def post_to_instagram(image_url, caption):
    # Step 1: Upload the media to Instagram
    upload_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    upload_response = requests.post(upload_url, data=payload)
    if upload_response.status_code != 200:
        print("Failed to upload media:", upload_response.json())
        return

    media_id = upload_response.json().get("id")
    print(f"Media uploaded successfully! Media ID: {media_id}")

    # Step 2: Publish the media
    publish_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    payload = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN
    }

    publish_response = requests.post(publish_url, data=payload)
    if publish_response.status_code == 200:
        print("Post published successfully!")
    else:
        print("Failed to publish post:", publish_response.json())


if __name__ == "__main__":
    # The photo you want to post
    IMAGE_URL = "https://i0.wp.com/www.bethel.k12.or.us/wp-content/uploads/2021/10/bigstock-147279827.jpg?fit=900%2C675&ssl=1"  # Publicly accessible image URL
    CAPTION = "caption for the Instagram post!"   # Caption for the post
    # Post the image
    post_to_instagram(IMAGE_URL, CAPTION)
