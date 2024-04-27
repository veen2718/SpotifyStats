import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import pytz
import json

from apikeys import client_id_spotify, client_secret_spotify


def timefix(spotify_timestamp):
    # Parse the timestamp as a UTC datetime object
    utc_time = datetime.strptime(spotify_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Define the UTC and PDT time zones
    utc_zone = pytz.timezone("UTC")
    pdt_zone = pytz.timezone("America/Los_Angeles")

    # Convert the timestamp to PDT
    utc_time = utc_zone.localize(utc_time)
    pdt_time = utc_time.astimezone(pdt_zone)
    return pdt_time.strftime("%Y-%m-%d %H:%M:%S")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_spotify,
                                               client_secret=client_secret_spotify,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"))



def get_tracks():
  tracks = []
  albums = []
  recent_tracks = sp.current_user_recently_played(limit=50)
  
  for track in recent_tracks['items']:
     artists = track['track']['artists']
     artists = [artists[i]['name'] for i in range(len(artists))]
     tracks.append({
        "endTime":timefix(track['played_at']),
        "trackName":track['track']['name'],
        "artistName":artists,
        "duration_ms":track['track']['duration_ms'],
        "msPlayed":None,
     })

     x = track

  print("Got tracks from Spotify API")
  return tracks


