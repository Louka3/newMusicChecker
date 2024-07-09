# gets .env file for access to variables
import os
from dotenv import load_dotenv, dotenv_values

# imports spotipy for spotofy api access
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import urllib.request
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

load_dotenv()

CLIENT_ID = os.getenv("APP_CLIENT_ID")
CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE")

def sendEmail(bands):
  EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
  EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
  TO_EMAIL = os.getenv("TO_EMAIL")
  FROM_EMAIL = os.getenv("FROM_EMAIL")
  
  email_subject = "New music from a band you like!"
  body = "Looks like there's new music from {bands}".format(bands=bands)
  
  msg = MIMEMultipart()
  msg['From'] = FROM_EMAIL
  msg['To'] = TO_EMAIL
  msg['Subject'] = email_subject

  msg.attach(MIMEText(body, 'plain'))

  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

    text = msg.as_string()
    server.sendmail(FROM_EMAIL, TO_EMAIL, text)
    server.quit()

    print("Email sent!")
  except Exception as e:
    print(f"Failed to send email: {e}")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE, 
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               cache_path=".cache"))

# get data from json file
with open('BandList.json', 'r') as file:
  jsonData = json.load(file)

#updating the album count if its changed
newMusic = []
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
    newMusic.append(band["name"])

if(len(newMusic) != 0):
  sendEmail(newMusic)

# write data back into the json file
with open('BandList.json', 'w') as file:
  json.dump(jsonData, file, indent=2)

print("Data has been updated!")
