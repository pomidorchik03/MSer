import asyncio
import json
import os
from spotipy import Spotify
from aiogram import Bot
from fan_management import load_fans_data
from spotify import sp

async def check_for_new_releases(bot: Bot):
    while True:
        try:
            data = load_fans_data()
            news = {}
            
            for user_id in data:
                news[user_id] = []
                for artist_id in data[user_id]:
                    latest_album = sp.artist_albums(artist_id, limit=1)
                    if not latest_album["items"]:
                        continue
                    
                    latest_album_id = latest_album["items"][0]["id"]
                    if data[user_id][artist_id] != latest_album_id:
                        news[user_id].append(artist_id)
                        data[user_id][artist_id] = latest_album_id
                
                if not news[user_id]:
                    news.pop(user_id)
            
            if news:
                with open("news.json", "w", encoding="utf-8") as f:
                    json.dump(news, f, indent=4, ensure_ascii=False)
                
                for user_id, artists in news.items():
                    try:
                        await bot.send_message(user_id, "🎉 У ваших любимых артистов вышли новые альбомы!")
                        for artist_id in artists:
                            artist_info = sp.artist(artist_id)
                            album_info = sp.album(sp.artist_albums(artist_id, limit=1)['items'][0]['id'])
                            await bot.send_message(
                                user_id,
                                f"🆕 {artist_info['name']} выпустил новый альбом:\n"
                                f"💿 {album_info['name']}\n"
                                f"📅 {album_info['release_date']}"
                            )
                    except Exception as e:
                        print(f"Ошибка уведомления {user_id}: {e}")
                
                with open("fans.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            
            await asyncio.sleep(6 * 60 * 60)  
        except Exception as e:
            print(f"Ошибка фоновой проверки: {e}")
            await asyncio.sleep(3600)  