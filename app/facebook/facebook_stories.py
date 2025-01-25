import requests

# Constants
page_id = '677777492613281'
access_token = 'EAAIqi2ZA41H4BO1HWd59UPm2ZAbLiIfWgBu1adi9Ab54hl2BbgtjBvTrMcSIzZAVRzyZAsnERsqmCERZAofU3hDEvm7ciI12ep1PwJxILpo9HX6GUJS4i72hhzRnNE2EZBKZBqVgfCSvKoJVrPDRFRNzy6swh7gITGeukQrLDcAcMrhZA3fQn1NGzAmABPY9W3nK'
photo_path = 'https://i0.wp.com/www.bethel.k12.or.us/wp-content/uploads/2021/10/bigstock-147279827.jpg?fit=900%2C675&ssl=1'

# Step 1: Upload the photo
url = f'https://graph.facebook.com/v22.0/{page_id}/photos'
payload = {
    'access_token': access_token,
    'published': 'false'  # Prevent it from being published as a regular post
}
files = {
    'file': open(photo_path, 'rb')
}
response = requests.post(url, data=payload, files=files)
photo_id = response.json().get('id')

# Step 2: Publish the photo as a story
url = f'https://graph.facebook.com/v22.0/{page_id}/photo_stories'
payload = {
    'access_token': access_token,
    'photo_id': photo_id
}
response = requests.post(url, data=payload)

if response.status_code == 200:
    print(f"Story posted successfully! Post ID: {response.json()['post_id']}")
else:
    print(f"Failed to post story: {response.text}")
