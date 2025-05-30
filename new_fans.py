import time
from spotipy import Spotify
from spotify_client import sp
import json
import os


def check_and_create_json(filename: str):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        with open(filename, "x") as f:
            json.dump({}, f)
        print("Файл создан с пустыми данными")


def get_last_release(artist_id: int) -> str:
    searched_albums = sp.artist_albums(artist_id)
    albums = searched_albums["items"]

    if not albums:
        print("Нет альбомов")
        return None

    sorted_albums = sorted(albums, key=lambda x: x["release_date"], reverse=True)

    last_release = sorted_albums[0]

    return last_release["id"]


def fan_request(user_id: int, artists: list):
    filename = "fans.json"
    check_and_create_json(filename)

    with open(filename, "r+") as check_list:

        check_list.seek(0)

        data = json.load(check_list)

        user_id_str = str(user_id)
        if user_id_str in data:
            print("Пользователь уже есть!")
            for artist in artists:
                if not (artist in data[user_id_str].keys()):
                    data[user_id_str][artist] = get_last_release(artist)
                    print("Добавляет любимых артистов")

        else:
            print("Добавляем нового пользователя")
            result = {artist: get_last_release(artist) for artist in artists}
            data[user_id_str] = result

        check_list.seek(0)
        check_list.truncate()
        json.dump(data, check_list, indent=4, ensure_ascii=False)