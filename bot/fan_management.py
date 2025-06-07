import json
import os
from spotify import get_last_release

def load_fans_data():
    filename = "fans.json"
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_fans_data(data: dict):
    filename = "fans.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_favorites(user_id: str, artist_ids: list):
    data = load_fans_data()
    if user_id not in data:
        data[user_id] = {}
    for artist_id in artist_ids:
        if artist_id not in data[user_id]:
            data[user_id][artist_id] = get_last_release(artist_id)
    save_fans_data(data)

def remove_favorite(user_id: str, artist_id: str):
    data = load_fans_data()
    if user_id in data and artist_id in data[user_id]:
        del data[user_id][artist_id]
        save_fans_data(data)
        return True
    return False

def get_favorites(user_id: str):
    data = load_fans_data()
    return data.get(str(user_id), {})