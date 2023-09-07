import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Path to the service account key JSON file
key_path = 'redditReelsServiceAccount.json'

# Define the scopes (permissions) you need
scopes = []#'https://www.googleapis.com/auth/calendar.readonly']

# Create credentials from the service account key file
credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=scopes
)

# If the token has expired, refresh it
if credentials.expired:
    credentials.refresh(Request())

# Access token for making API requests
access_token = credentials.token
print(f'Access Token: {access_token}')
