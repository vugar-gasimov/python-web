import os
import spotipy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv(dotenv_path="Hot-100/.env")

# Validate environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

if not all([client_id, client_secret, redirect_uri]):
    logging.error("Missing one or more Spotify credentials in the environment variables.")
    exit()

def get_billboard_hot_100(date):
    """Fetch Billboard Hot 100 songs for a given date."""
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        logging.error(f"Failed to retrieve Billboard Hot 100 page. Status code: {response.status_code}")
        exit()
        
    soup = BeautifulSoup(response.text, "html.parser")
    songs = soup.select(selector="li ul li h3")
    song_names = [song.getText().strip() for song in songs]
    return song_names

def create_spotify_playlist(user_id, playlist_name, playlist_description):
    """Create a Spotify playlist."""
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path=fr"Hot-100\token.txt"
        )
    )
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False, description=playlist_description)
    return playlist["id"], sp

def add_songs_to_playlist(sp, playlist_id, song_names, year):
    """Search for songs on Spotify and add them to the playlist."""
    track_uris = []
    for song_name in song_names:
        results = sp.search(q=f"track:{song_name} year:{year}", limit=1, type='track')
        try:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
        except (IndexError, KeyError):
            logging.warning(f"Song '{song_name}' not found on Spotify.")
    
    if track_uris:
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        logging.info(f"Added {len(track_uris)} tracks to the playlist.")
    else:
        logging.warning("No tracks found to add to the playlist.")

def main():
    user_date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

    try:
        datetime.strptime(user_date_input, "%Y-%m-%d")
    except ValueError:
        logging.error("Invalid date format. Please enter YYYY-MM-DD.")
        exit()

    song_names = get_billboard_hot_100(user_date_input)
    logging.info(f"Retrieved {len(song_names)} songs from Billboard Hot 100 for {user_date_input}")

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path=fr"Hot-100\token.txt"
        )
    )
    
    user_id = sp.current_user()["id"]
    year = user_date_input.split("-")[0]

    playlist_name = f"Billboard Hot 100 - {year}"
    playlist_description = f"Billboard Hot 100 songs from {year}"
    playlist_id, sp = create_spotify_playlist(user_id, playlist_name, playlist_description)

    add_songs_to_playlist(sp, playlist_id, song_names, year)
    logging.info("Playlist created successfully.")

if __name__ == "__main__":
    main()