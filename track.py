from spotify_client import sp
from genius_client import *


def convert_ms_to_time(ms):
    seconds = ms // 1000 
    hours = seconds // 3600 
    seconds %= 3600 
    minutes = seconds // 60 
    seconds %= 60  


    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"


async def track_search(track_name: str, limit: int = 10):
    results = sp.search(q=track_name, type='track', limit=limit)
    tracks = results['tracks']['items']
    if not tracks:
        print("Ничего не найдено :(")
        return
    return [
        {
            "id": track["id"],
            "name": track["name"],
            "artists": ", ".join([a["name"] for a in track["artists"]]),
            "duration": convert_ms_to_time(track["duration_ms"])
        }
        for track in results["tracks"]["items"]
    ]

    