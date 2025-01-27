#https://developers.facebook.com/docs/page-stories-api/
from dotenv import load_dotenv
import os
import requests

import ssl
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import subprocess

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

def video_post(video_path,message=None):
    # Step 1: Initiate upload
    chunk_size = 1024*1024*4
    initiate_params = {
        "access_token": ACCESS_Token,
        "upload_phase": "start",
        "file_size": os.path.getsize(video_path)
    }

    initiate_response = requests.post(f"{API_URL}/videos", data=initiate_params)
    if initiate_response.status_code != 200:
        print("Failed to initiate video upload.")
        print(initiate_response.json())
        exit()

    upload_session_id = initiate_response.json()["upload_session_id"]
    video_id = initiate_response.json()["video_id"]
    print(f"Upload session initiated. Session ID: {upload_session_id}, Video ID: {video_id}")

    # Step 2: Upload chunks
    with open(video_path, "rb") as video_file:
        start_offset = 0
        while True:
            video_file.seek(start_offset)
            chunk = video_file.read(chunk_size)
            if not chunk:
                break

            
            upload_params = {
                "access_token": ACCESS_Token,
                "upload_phase": "transfer",
                "upload_session_id": upload_session_id,
                "start_offset": start_offset
            }
            files = {
                "video_file_chunk": chunk
            }

            upload_response = requests.post(f"{API_URL}/videos", data=upload_params, files=files)
            if upload_response.status_code != 200:
                print("Failed to upload chunk.")
                print(upload_response.json())
                exit()

            upload_data = upload_response.json()
            start_offset = int(upload_data["start_offset"])
            end_offset = int(upload_data["end_offset"])

            print(f"Uploaded chunk. Start offset: {start_offset}, End offset: {end_offset}")
            if start_offset == end_offset:
                break

    # Step 3: Finalise upload
    finalise_params = {
        "access_token": ACCESS_Token,
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        "description": message
    }

    finalise_response = requests.post(f"{API_URL}/videos", data=finalise_params)
    if finalise_response.status_code == 200:
        print("Video upload complete!")
        print("Response:", finalise_response.json())
    else:
        print("Failed to finalise video upload.")
        print(finalise_response.json())

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
        print("Failed to upload video in stories!")
        print("Error:", response.json())
    
def video_stories(video_url):
    # Step 1: Start the video upload session
    payload = {
    "upload_phase": "start",
    "access_token":ACCESS_Token,
     }
       
    response = requests.post(f"{API_URL}/video_stories", data=payload)
    print(f'response = {response.json()}')
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


def reel_upload(video_file):
    ACCESS_Token = "EAAIqi2ZA41H4BOZByhfZCpfMNA6gIumkZCFL473xs411iNZBzMG4lxDPOZBnY0mM2pt5Lq8W43rRqeZCiLTfeTtMcyUebumZBrcZBWq4BiAOnVWifRGyQfwZBTVaqMZAyM1mPZBu6AVWo9N8iaCnF9NAYKMqWJuvqe9AwqZAGDeBhJwcZBHFjswzKPs3jZCZAEJQ9jeg6NAIrSnY8vzST2S464zTTAZDZD"
    #Initiate the Upload Session
    payload = {
        "upload_phase": "start",
        "access_token":f'OAuth   {ACCESS_Token}',
     }

    response = requests.post(f"{API_URL}/video_reels",data=payload)
    video_id = response.json().get("video_id")
    upload_url = response.json().get("upload_url")
    print(f'video_id = {video_id} \n upload url = {upload_url}')

    #upload the video
    file_size = os.path.getsize(video_file)
    headers = {
        'access_token': f'OAuth  {ACCESS_Token}',
        'offset': str(0),
        'file_size': str(file_size),
    }
    with open(video_file, "rb") as file:
        file_data = file.read()
        upload_url1 = f'https://rupload.facebook.com/video-upload/v13.0/{video_id}'
        response = requests.post(upload_url1, headers=headers, data=file_data)
        print(response.json())  # Check the response from the upload


if __name__ == "__main__":
  #  message_post("Hello, world! 😊🎉🚀")
    load_dotenv()
    print(f'{ACCESS_Token}')
   # photo_stories("https://i0.wp.com/www.bethel.k12.or.us/wp-content/uploads/2021/10/bigstock-147279827.jpg?fit=900%2C675&ssl=1")
    #video_post(r"C:\Users\Fission\Downloads\test.mp4")
    reel_upload(r"C:\Users\Fission\Downloads\test.mp4")