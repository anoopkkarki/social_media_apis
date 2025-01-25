#https://developers.facebook.com/docs/page-stories-api/
from dotenv import load_dotenv
import os
import requests

load_dotenv()


ACCESS_Token = os.getenv("ACCESS_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")
API_URL=f"https://graph.facebook.com/v21.0/{PAGE_ID}"

def message_post(message):

    payload = {
        "message":message,
        "access_token":ACCESS_Token,
    }
    response = requests.post(f"{API_URL}/feed",data=payload)
    if response.status_code == 200:
        print("post successfull :",response.json())
    else:
        print("error :",response.json())

def photo_post(photo_url,message=None):
    load_dotenv()
    payload = {
    "caption":message,
    "access_token":ACCESS_Token,
    "url": photo_url,
    }
    if message:
        payload["caption"] = message
        
    response = requests.post(f"{API_URL}/photos", data=payload)

    # Check the response
    if response.status_code == 200:
        print("Photo uploaded successfully!")
        print("Response:", response.json())
    else:
        print("Failed to upload photo!")
        print("Error:", response.json())
    

def photo_stories(photo_url):
    payload = {
    'published': 'false',  # Prevent it from being published as a regular post
    "access_token":ACCESS_Token,
    "url": photo_url,
    }
       
    response = requests.post(f"{API_URL}/photos", data=payload)
    photo_id = response.json().get('id')

    # Step 2: Publish the photo as a story
    
    payload = {
        'access_token': ACCESS_Token,
        'photo_id': photo_id
    }
    response = requests.post(f"{API_URL}/photo_stories", data=payload)

    # Check the response
    if response.status_code == 200:
        print("Photo uploaded successfully!")
        print("Response:", response.json())
    else:
        print("Failed to upload photo!")
        print("Error:", response.json())
    



def video_stories(video_url):
    # Step 1: Start the video upload session
    payload = {
    "upload_phase": "start",
    "access_token":ACCESS_Token,
     }
       
    response = requests.post(f"{API_URL}/video_stories", data=payload)
    print(f'response = {response.json()}')
    '''if response.status_code != 200:
        print("Failed to initialize upload!")
        print('i am just in if elese')
        print("Error:", response.json())
    return'''
    print(f'i am just outside if else')
    video_id = response.json().get('video_id')
    print(f'video_id = {video_id}')
    upload_url = response.json().get('upload_url')
#------------------------------------------------------------------
    # Step 2: Upload the video
    file_size = os.path.getsize(video_url)
    print(f'file_size= {file_size}')
    with open(video_url, "rb") as video_file:
        
        headers = {
            'offset': '0',
            'file_size': str(file_size),
        }
        upload_response = requests.post(upload_url, headers=headers, data=video_file)
        print(f'upload_response_ofsett = {upload_response.json()}')
        
        if upload_response.status_code != 200:
            print("Failed to upload video!")
            print("Error:", upload_response.json())
            return

# Step 3: Publish the video as a story
    publish_payload = {
        "access_token": ACCESS_Token,
        "video_id": video_id,
        "upload_phase": "finish",
    }
    publish_response = requests.post(f"{API_URL}/video_stories", data=publish_payload)

# Check the response
    if publish_response.status_code == 200:
        print("Video story uploaded successfully!")
        print("Response:", publish_response.json())
    else:
        print("Failed to publish video story!")
        print("Error:", publish_response.json())

if __name__ == "__main__":
  #  message_post("Hello, world! 😊🎉🚀")
    load_dotenv()
    print(f'{ACCESS_Token}')
   # photo_stories("https://i0.wp.com/www.bethel.k12.or.us/wp-content/uploads/2021/10/bigstock-147279827.jpg?fit=900%2C675&ssl=1")
    video_stories(r"C:\Users\Fission\Downloads\test.mp4")