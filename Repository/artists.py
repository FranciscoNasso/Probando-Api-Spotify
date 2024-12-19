import pandas as pd
from Services.utils import initialize_spotify

import time


# Initialize Spotipy
sp = initialize_spotify() 


def get_artist_tracks(artists, limit): 
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

    enriched_tracks = sorted(enriched_tracks, key=lambda t: t['popularity'], reverse=True)

    df_tracks = pd.DataFrame(enriched_tracks)
    filename = f'Enriched_Data/Songs_From_Artists/{artists}-songs.csv'
    df_tracks.to_csv(filename, index=False, encoding='utf-8')

    return df_tracks.sort_values(by='popularity', ascending=False).head(limit).to_dict(orient='records')


def get_all_albums_from_artists(artist_name):
    results = sp.search(q=f'artist:"{artist_name}"', type='artist', limit=10)
    if 'artists' not in results or 'items' not in results['artists'] or not results['artists']['items']:
            print(f"No se encontró el artista: {artist_name}")
            return []
    
    artist = max(results['artists']['items'], key=lambda a: a['popularity'])
    artist_id = artist['id']

    albums = sp.artist_albums(artist_id, album_type='album')
    albums_df = pd.DataFrame(albums['items'])
    filename = f'Enriched_Data/Albums/{artist_name}-albums.csv'
    albums_df.to_csv(filename, index=False, encoding='utf-8')
    return albums_df.to_dict(orient='records')


def get_artist_genres(artist_name):
    results = sp.search(q=f'artist:"{artist_name}"', type='artist', limit=10)
    if 'artists' not in results or 'items' not in results['artists'] or not results['artists']['items']:
            print(f"No se encontró el artista: {artist_name}")
            return []
    
    artist = max(results['artists']['items'], key=lambda a: a['popularity'])
    artists_genre = artist['genres']

    genre_data = [{'genre': genre} for genre in artists_genre]
    
    genre_df = pd.DataFrame(genre_data)

    filename = f'Enriched_Data/Genres_Artists/{artist_name}-genres.csv'
    genre_df.to_csv(filename, index=False, encoding='utf-8')
    return genre_df.to_dict(orient='records')


#popular_albums = get_all_albums_from_artists('Kanye West')

artist_genres = get_artist_genres('The Weeknd')

