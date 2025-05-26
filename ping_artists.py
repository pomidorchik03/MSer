import time
from spotipy import Spotify
from spotify_client import sp
from new_fans import get_last_release, check_and_create_json
import json


def check_news():
    filename_fans = "fans.json"
    # check_and_create_json(filename_fans)
    with open(filename_fans, "r", encoding="utf-8") as file:

        data = json.load(file)

        filename_news = "news.json"
        check_and_create_json(filename_news)



        with open(filename_news, "w", encoding="utf-8") as news_for_fans:

            news = {}

            for user_id in data:

                news[user_id] = []

                for art in data[user_id]:

                    last_album = get_last_release(art)
                    curr_album = data[user_id][art]
                    
                    if last_album != curr_album:

                        print("Есть обновление!")
                        news[user_id].append(art)
                        data[user_id][art] = last_album



                if not news[user_id]:

                    news.pop(user_id)

            json.dump(news, news_for_fans, indent = 4, ensure_ascii = False)
        
        with open(filename_fans, "w") as updated_file:
            json.dump(data, updated_file, indent = 4, ensure_ascii = False)
