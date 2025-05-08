from spotify_client import sp
from album import *

def artist_search(query, limit = 10): #функция для поиска артиста
    results = sp.search(q=query, type='artist', limit=limit)
    artists = results['artists']['items']
    
    if not artists:
        print("Ничего не найдено :(")
        return
    print(f"Результаты для '{query}':\n")
    
    for idx, artist in enumerate(artists, 1):
        name = artist['name']
        artist_id = artist['id']
        print(f"{idx}. {name}")

    print("Выберите артиста из списка(Если вашего артиста нет в списке, измените запрос или дополните его)")
    choice = int(input())
    select_artist = artists[choice - 1]
    artist_info(select_artist['id'])

    print(f'Хотите получить список альбомов? 1 - да, 2 - нет')
    hochy = int(input())
    if(hochy == 1):
        artist_albums(select_artist['id'])
    else: return

def artist_info(artist_id): #функция для получения информации об артисте
    artist = sp.artist(artist_id)

    # Извлечение данных
    name = artist['name']
    genres = ', '.join(artist['genres']) if artist['genres'] else 'не указаны'
    popularity = artist['popularity']
    followers = f"{artist['followers']['total']:,}"

    # Вывод информации
    print(f"Имя артиста: {name}")
    print(f"Жанры: {genres}")
    print(f"Популярность на Spotify: {popularity}/100")
    print(f"Количество подписчиков: {followers}")


