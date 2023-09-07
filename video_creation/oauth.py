# import os
# from google.oauth2 import service_account
# from google.auth.transport.requests import Request

# # Path to the service account key JSON file
# key_path = 'serviceAccount/redditReelsServiceAccount.json'

# # Define the scopes (permissions) you need
# scopes = ['https://www.googleapis.com/auth/youtube.upload']

# # Create credentials from the service account key file
# credentials = service_account.Credentials.from_service_account_file(
#     key_path, scopes=scopes
# )

# # If the token has expired, refresh it
# if credentials.expired:
#     credentials.refresh(Request())

# # Access token for making API requests
# access_token = credentials.token
# print(f'Access Token: {access_token}')



import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# Path to your OAuth 2.0 credentials JSON file
credentials_file = 'accountCredentials\client_secret_205473897086-857rs2bdut37ssspvs2a3vl37cifef6i.apps.googleusercontent.com.json'
# Path to the video file you want to upload
video_file = 'path/to/your/video.mp4'

# Load the credentials
creds = Credentials.from_authorized_user_file(credentials_file)

# Create a YouTube Data API client
youtube = build('youtube', 'v3', credentials=creds)

# Upload video
request_body = {
    'snippet': {
        'title': 'Your Video Title',
        'description': 'Your Video Description',
        'tags': ['tag1', 'tag2'],
        'categoryId': '22'  # You can find category IDs on the YouTube website
    },
    'status': {
        'privacyStatus': 'private'  # Change to 'public' if you want the video to be public
    }
}

media = MediaFileUpload(video_file)
youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()
