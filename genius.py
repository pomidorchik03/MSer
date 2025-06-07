import lyricsgenius
from config import GENIUS_ACCESS_TOKEN

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=10, skip_non_songs=True)

async def get_lyrics(song_name: str, artist_name: str):
    try:
        song = genius.search_song(song_name, artist_name)
        return song.lyrics.strip() if song and song.lyrics else None
    except Exception as e:
        print(f"Ошибка при поиске текста для {song_name} от {artist_name}: {e}")
        return None