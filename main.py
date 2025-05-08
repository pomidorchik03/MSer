from track import *
from artist import *

print(f'Че хотите? Поиск трека - 1, поиск артиста - 2')
choose = int(input())

if(choose == 1):
    print(f'Введите название трека')
    trackname = input()
    track_search(trackname)
elif(choose == 2):
    print(f'Введите имя артиста')
    artistname = input()
    artist_search(artistname)