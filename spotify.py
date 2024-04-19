from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import sys
import config 

scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, client_id=config.SPOTIFY_CLIENT,
                     client_secret=config.SPOTIFY_CLIENT_SECRET, redirect_uri = "http://localhost:9988/callback"))

result = sp.search("faded", limit=1)

uri = result['tracks']['items'][0]['album']['artists'][0]['uri']
print(uri)

res = sp.devices()

sp.start_playback(uris=[uri])

sp.volume(100)
sleep(2)
sp.volume(10)
sleep(2)
sp.volume(20)