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


def track_search(track_name, limit=10): #функция для поиска трека
    results = sp.search(q=track_name, type='track', limit=limit)
    tracks = results['tracks']['items']
    if not tracks:
        print("Ничего не найдено :(")
        return
    
    print(f"10 самых популярных треков по запросу '{track_name}':\n")
    for idx, track in enumerate(tracks, 1):
        artists = ", ".join([a['name'] for a in track['artists']])
        print(f"{idx}. {track['name']} — {artists}")

    print(f"Если вашего трека нет в списке, измените или дополните запрос")

    print("Хотите получить информацию об определенном треке?(1 - всю информацию кроме текста, 2 - только текст, 3 - нет)") #По идее это убрать надо будет, пользователь зачем трек ищет если не для информации
    hochy = int(input())
    if(hochy == 1):
        print("Выберите трек")
        choice = int(input())
        track_id = tracks[choice - 1]['id']
        track_info(track_id)
    elif(hochy == 2):
        song = genius.search_song(results)
        print(song.lyrics)
    else:
        return

    
def track_info(track_id): #функция для инфы по треку

    track = sp.track(track_id)

    # Извлечение данных
    track_name = track['name']
    artists = ', '.join([artist['name'] for artist in track['artists']])
    album_name = track['album']['name']
    album_release_date = track['album']['release_date']
    duration = convert_ms_to_time(track['duration_ms'])
    popularity = track['popularity']
    
    print(f"Название трека: {track_name}")
    print(f"Исполнители: {artists}")
    print(f"Альбом: {album_name}")
    print(f"Дата выхода: {album_release_date}")
    print(f"Длительность: {duration}")
    print(f"Индекс популярности Spotify: {popularity}")