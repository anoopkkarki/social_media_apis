import requests
from dotenv import load_dotenv
import os

load_dotenv()


# Replace with your details
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Image or video URL for the story (publicly accessible)
STORY_URL = "https://i0.wp.com/www.bethel.k12.or.us/wp-content/uploads/2021/10/bigstock-147279827.jpg?fit=900%2C675&ssl=1"

def post_instagram_story(story_url):
    # Step 1: Upload media as a story
    upload_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "image_url": story_url,  # Replace with "video_url" if uploading a video
        "media_type": "STORIES",  # Specifies this is a story
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(upload_url, data=payload)
    if response.status_code != 200:
        print("Failed to upload story:", response.json())
        return

    media_id = response.json().get("id")
    print(f"Story uploaded! Media ID: {media_id}")

    # Step 2: Publish the story
    publish_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    payload = {
        "creation_id": media_id,
        "access_token": ACCESS_TOKEN
    }

    publish_response = requests.post(publish_url, data=payload)
    if publish_response.status_code == 200:
        print("Story published successfully!")
    else:
        print("Failed to publish story:", publish_response.json())

# Call the function
post_instagram_story(STORY_URL)
