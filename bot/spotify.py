import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from helpers import convert_ms_to_time

def init_spotify():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))

# Глобальный клиент
sp = init_spotify()

#Поиск артиста по ID
def get_last_release(artist_id: int) -> str:
    searched_albums = sp.artist_albums(artist_id)
    albums = searched_albums["items"]
    if not albums:
        print("Нет альбомов")
        return None
    sorted_albums = sorted(albums, key=lambda x: x["release_date"], reverse=True)
    last_release = sorted_albums[0]
    return last_release["id"]

# Поиск треков
async def track_search(query: str, limit: int = 10):
    results = sp.search(q=query, type="track", limit=limit)
    tracks = results["tracks"]["items"]
    if not tracks:
        return []
    return [{
        "id": track["id"],
        "name": track["name"],
        "artists": ", ".join([a["name"] for a in track["artists"]]),
        "duration": convert_ms_to_time(track["duration_ms"])
    } for track in tracks]

# Поиск артистов
async def artist_search(query: str, limit: int = 10):
    results = sp.search(q=query, type="artist", limit=limit)
    artists = results["artists"]["items"]
    if not artists:
        return []
    return [{
        "id": artist["id"],
        "name": artist["name"],
        "genres": ", ".join(artist.get("genres", ["не указаны"])),
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"]
    } for artist in artists]

#Поиск артистов для 
async def find_artist_by_name(artist_name: str):
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results["artists"]["items"]:
        return None
    return results["artists"]["items"][0]["id"]

# Информация об артисте
async def get_artist_info(artist_id: str):
    return sp.artist(artist_id)

# Альбомы артиста
async def get_artist_albums(artist_id: str):
    return sp.artist_albums(artist_id, limit=20)

# Треки альбома
async def get_album_tracks(album_id: str):
    return sp.album_tracks(album_id)

# Информация о треке
async def get_track_info(track_id: str):
    return sp.track(track_id)