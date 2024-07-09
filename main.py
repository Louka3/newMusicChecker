# gets .env file for access to variables
import os
from dotenv import load_dotenv, dotenv_values

# imports spotipy for spotofy api access
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json

# import urllib.request
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

load_dotenv()

CLIENT_ID = os.getenv("APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")

SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, 
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               cache_path=".cache"))
# get data from json file
with open('BandList.json', 'r') as file:
  jsonData = json.load(file)

#updating the album count if its changed
for band in jsonData["bands"]:
  results = sp.search(q=band["name"], type='artist')
  res = sp.artist_albums(results["artists"]["items"][0]['uri'], include_groups='album,single', limit=20)
  count = 0
  isNext = True
  while(isNext):
    for item in res['items']:
      count += 1
    if(res['next']):
      res = sp.next(res)
      continue
    else:
      isNext = False
  if(count != band["albums"]):
    band["albums"] = count

# write data back into the json file
with open('BandList.json', 'w') as file:
  json.dump(jsonData, file, indent=2)

print("data has been updated")


# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])

# for album in albums:
#     print(album['name'])