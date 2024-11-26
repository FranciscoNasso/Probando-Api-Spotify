import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get credentials
client_id = os.getenv("spotify_Client_ID")
client_secret = os.getenv("spotify_Client_Secret")

# Initialize Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def get_mosts_popular_tracks_by_artists(artists, limit): 
    results = sp.search(q=f'artist:"{artists}"', type='artist', limit=10)
    if 'artists' not in results or 'items' not in results['artists'] or not results['artists']['items']:
            print(f"No se encontró el artista: {artists}")
            return []

    artist = max(results['artists']['items'], key=lambda a: a['popularity'])
    artist_id = artist['id']

    albums = sp.artist_albums(artist_id, album_type='album')

    track_ids = []

    for album in albums['items']:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            track_ids.append(track['id'])
    
    enriched_tracks = []

    for i in range(0, len(track_ids), 50):
        batch_ids = track_ids[i:i + 50]
        try:
            tracks = sp.tracks(batch_ids)['tracks']
            for track in tracks:
                if track:  # Verifica que el track no sea None
                    enriched_tracks.append({
                        'id': track['id'],
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'album': track['album']['name'],
                        'release_date': track['album']['release_date'],
                        'popularity': track.get('popularity', 0),
                        'duration_ms': track['duration_ms'],
                        'explicit': track['explicit']
                    })
        except Exception as e:
            print(f"Error al procesar lote {i // 50 + 1}: {e}")
            time.sleep(5)  # Retraso en caso de error

        # Retraso opcional para evitar límite de tasa de la API
        time.sleep(1)

    df_tracks = pd.DataFrame(enriched_tracks)
    filename = f'Enriched_Data/{artists}-songs.csv'
    df_tracks.to_csv(filename, index=False, encoding='utf-8')

    return df_tracks.sort_values(by='popularity', ascending=False).head(limit)



popular_tracks = get_mosts_popular_tracks_by_artists('Taylor Swift', 10)

