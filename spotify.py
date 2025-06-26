import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from helpers import convert_ms_to_time

def init_spotify():
    '''Инициализация API'''
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))


sp = init_spotify()


def get_last_release(artist_id: int) -> str:
    '''Возврат ID последнего релиза '''
    searched_albums = sp.artist_albums(artist_id)
    albums = searched_albums["items"]
    if not albums:
        print("Нет альбомов")
        return None
    sorted_albums = sorted(albums, key=lambda x: x["release_date"], reverse=True)
    last_release = sorted_albums[0]
    return last_release["id"]


async def track_search(query: str, limit: int = 10):    
    '''Поиск треков и возврат списка с ними'''
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


async def artist_search(query: str, limit: int = 10):
    '''Поиск артистов и возврат списка с ними'''
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


async def find_artist_by_name(artist_name: str):
    '''Поиск артиста по имени'''
    results = sp.search(q=artist_name, type="artist", limit=1)
    if not results["artists"]["items"]:
        return None
    return results["artists"]["items"][0]["id"]


async def get_artist_info(artist_id: str):
    '''Инфа а артиста'''
    return sp.artist(artist_id)


async def get_artist_albums(artist_id: str):
    '''Альбомы артиста'''
    return sp.artist_albums(artist_id, limit=20)


async def get_album_tracks(album_id: str):
    '''Треки альбома'''
    return sp.album_tracks(album_id)


async def get_track_info(track_id: str):
    '''Инфа о треке'''
    return sp.track(track_id)