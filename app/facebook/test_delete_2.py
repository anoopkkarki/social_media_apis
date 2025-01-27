import requests

# Replace these with your details
page_id = "677777492613281"
access_token = "EAAIqi2ZA41H4BO0VdSs58EXS77ZBumHxtUYymtJeZACbVEgwNzygZBXjmBickuzxzDNuq9ggIduZApwz9aWlC4IECG6j2ft4zqA5ZB6kasNt8xJKbyBljxzFOaoVLTjlVML8otlffmAvZCAZAHW0I1yVpkTsDV1Vi6qGgQJv5UgUcoTcLniY08XVgnJcXZCanHh0K"
video_path = "C:\\Users\\Fission\\Downloads\\test.mp4"  # Replace with the path to your video file
caption = "Your video caption here"

# Facebook Graph API endpoint for uploading videos
url = f"https://graph.facebook.com/v15.0/{page_id}/videos"

# Open the video file in binary mode
with open(video_path, "rb") as video_file:
    # Data for the API request
    data = {
        "access_token": access_token,
        "description": caption,
    }
    # Files to upload
    files = {
        "source": video_file,
    }

    # Send the POST request
    response = requests.post(url, data=data, files=files)

# Check the response
if response.status_code == 200:
    print("Video uploaded successfully!")
    print("Response:", response.json())
else:
    print("Failed to upload video.")
    print("Error:", response.json())