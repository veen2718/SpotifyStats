import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import pytz
import json

from apikeys import client_id, client_secret

with open('history.json','r') as historyjson:
   jsondata = json.loads(historyjson.read())
   finalDate = jsondata[len(jsondata)-1]['endTime']

print(finalDate)
# Set up the Spotify OAuth handler
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"))

# Get the user's recently played tracks
recent_tracks = sp.current_user_recently_played(limit=50)


# for track in recent_tracks['items']:
#    for i in track:
#       print(i,track[i])
#       print()
#       if type(i) is dict:
#          for j in i:
#             print(j,i[j])
#             print("-")
#    print("\n\n\n")



def expand(d,tab):
    print()
    if type(d) is dict:
      expand(d,tab + "  ")
    else:
      print(tab + str(d))


#expand(recent_tracks['items'],"")


def timefix(spotify_timestamp):
    # Example timestamp from Spotify API
    # Parse the timestamp as a UTC datetime object
    utc_time = datetime.strptime(spotify_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Define the UTC and PDT time zones
    utc_zone = pytz.timezone("UTC")
    pdt_zone = pytz.timezone("America/Los_Angeles")

    # Convert the timestamp to PDT
    utc_time = utc_zone.localize(utc_time)
    pdt_time = utc_time.astimezone(pdt_zone)
    return pdt_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

for track in recent_tracks['items']:
    print(timefix(track['played_at']), track['track']['name'], "-", track['track']['artists'][0]['name'])