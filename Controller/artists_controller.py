from fastapi import APIRouter
from fastapi.responses import JSONResponse

from Services import artists_services as artists_service

router = APIRouter()

@router.get("/artists/tracks")
async def get_artist_tracks(artist_name: str, limit: int = 10):
    return artists_service.get_artist_tracks(artist_name, limit)

@router.get("/artists/albums")
async def get_all_albums_from_artists(artist_name: str):
    return artists_service.get_all_albums_from_artists(artist_name)

@router.get("/artists/genres")
async def get_artist_genres(artist_name: str):
    return artists_service.get_artist_genres(artist_name)

