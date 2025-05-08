from spotify_client import sp
from track import *

def artist_albums(artist_id):
    albums_data = sp.artist_albums(artist_id, limit = 50)
    albums = albums_data['items']
    
    if not albums:
        print("У этого артиста пока нет альбомов.")
        return
    
    print(f"\nАльбомы артиста:")
    for idx, album in enumerate(albums, 1):
            name = album['name']
            album_type = album['album_type'].capitalize()
            release_date = album['release_date']
            total_tracks = album['total_tracks']

            print(f"{idx}. {name}")
            print(f"   Тип: {album_type}")
            print(f"   Дата выхода: {release_date}")
            print(f"   Количество треков: {total_tracks}")

    print('Хотите получить информацию по определенному альбому?')
    hochy = int(input())
    if(hochy == 1):
        print('выберите альбом из списка')
        choice = int(input())
        album_id = albums[choice - 1]['id']
        album_tracks(album_id)

def album_tracks(album_id):
    tracks_data = sp.album_tracks(album_id)
    tracks = tracks_data['items']
    print("\nТреки альбома:")
    for idx, track in enumerate(tracks, 1):
            name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            print(f"{idx}. {name} — {artists}")

    print("\nХотите получить подробную информацию о каком-то треке? (1 - да, 2 - нет)")
    choice = int(input())
    if(choice == 1):
        print(f'Введите номер трека:')
        track_num = int(input())
        select_track = tracks[track_num - 1]
        track_id = select_track['id']
        track_info(track_id)