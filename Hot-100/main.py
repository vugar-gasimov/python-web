import os
import spotipy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(dotenv_path="Hot-100/.env")

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

user_date_input = input("Which year do you want to travel to ? Type the date in this format YYYY-MM-DD:")

try:
    datetime.strptime(user_date_input, "%Y-%m-%d")
except ValueError:
    print("Invalid date format. Please enter YYYY-MM-DD.")
    exit()

ORIGINAL_URL = "https://www.billboard.com/charts/hot-100/2000-08-12/"
NEW_URL = "https://www.billboard.com/charts/hot-100/" + user_date_input + "/"

response = requests.get(NEW_URL)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.title)

# songs = soup.find_all(name="h3", id="title-of-a-story")
songs = soup.select(selector="li ul li h3")
song_names = [song.getText().strip() for song in songs]
print(song_names)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path=fr"Hot-100\token.txt",
        username="Billboard to Spotify", 
    )
)
user_id = sp.current_user()["id"]
year = user_date_input.split("-")[0]

playlist_name = f"Billboard Hot 100 - {year}"
playlist_description = f"Billboard Hot 100 songs from {year}"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)
playlist_id = playlist["id"]

track_uris = []
for song_name in song_names:
    results = sp.search(q=f"track:{song_name} year:{year}", limit=1, type='track')
    try:
        track_uri = results['tracks']['items'][0]['uri']
        track_uris.append(track_uri)
    except (IndexError, KeyError):
        print(f"Song '{song_name}' not found on Spotify.")

if track_uris:
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
    print(f"Added {len(track_uris)} tracks to the playlist '{playlist_name}'.")

print("Playlist created successfully.")

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=client_id,
#     client_secret=client_secret,
#     redirect_uri=redirect_uri))

# playlists = sp.current_user_playlists()
# for playlist in playlists['items']:
#     print(playlist['name'])