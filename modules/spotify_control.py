import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

def play_song(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        track_uri = tracks[0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"🎵 Playing: {song_name}")
    else:
        print("❌ Song not found.")

def pause_music():
    sp.pause_playback()
    print("⏸️ Music paused.")

def resume_music():
    sp.start_playback()
    print("▶️ Music resumed.")

def stop_music():
    sp.pause_playback()
    print("⏹️ Music stopped.")  # Same as pause, but semantically "stop"
