from Repository import artists as artists_data

def get_artist_tracks(artist_name, limit):
    return artists_data.get_artist_tracks(artist_name, limit)

def get_all_albums_from_artists(artist_name):
    return artists_data.get_all_albums_from_artists(artist_name)

def get_artist_genres(artist_name):
    return artists_data.get_artist_genres(artist_name)

