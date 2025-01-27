import os
import requests

# Replace with your details
PAGE_ID = "677777492613281"
access_token = "EAAIqi2ZA41H4BO0VdSs58EXS77ZBumHxtUYymtJeZACbVEgwNzygZBXjmBickuzxzDNuq9ggIduZApwz9aWlC4IECG6j2ft4zqA5ZB6kasNt8xJKbyBljxzFOaoVLTjlVML8otlffmAvZCAZAHW0I1yVpkTsDV1Vi6qGgQJv5UgUcoTcLniY08XVgnJcXZCanHh0K"
video_path = "C:\\Users\\Fission\\Downloads\\test.mp4"  # Replace with the path to your video file
caption = "Your video caption here"
chunk_size = 1024 * 1024 * 4  # 4 MB per chunk (recommended)
API_URL=f"https://graph.facebook.com/v21.0/{PAGE_ID}"


def video_post(video_path,caption = None):
    # Step 1: Initiate upload
    initiate_params = {
        "access_token": access_token,
        "upload_phase": "start",
        "file_size": os.path.getsize(video_path)
    }

    initiate_response = requests.post(f"{API_URL}/video_reels", data=initiate_params)
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

            #upload_url = f"https://graph.facebook.com/v15.0/{PAGE_ID}/videos"
            upload_params = {
                "access_token": access_token,
                "upload_phase": "transfer",
                "upload_session_id": upload_session_id,
                "start_offset": start_offset
            }
            files = {
                "video_file_chunk": chunk
            }

            upload_response = requests.post(f"{API_URL}/video_reels", data=upload_params, files=files)
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
        "access_token": access_token,
        "upload_phase": "finish",
        "upload_session_id": upload_session_id,
        "description": caption
    }

    finalise_response = requests.post(f"{API_URL}/videos", data=finalise_params)
    if finalise_response.status_code == 200:
        print("Video upload complete!")
        print("Response:", finalise_response.json())
    else:
        print("Failed to finalise video upload.")
        print(finalise_response.json())

if __name__ == "__main__":
    video_post("C:\\Users\\Fission\\Downloads\\test.mp4")