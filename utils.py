from dotenv import load_dotenv
import os

from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify


def initialize_spotify():
    load_dotenv()

    client_id = os.getenv('spotify_Client_ID')
    client_secret = os.getenv('spotify_Client_Secret')

    if not client_id or not client_secret:
        raise ValueError("Spotify Client ID and Client Secret are required")
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return Spotify(auth_manager=auth_manager)

