import lyricsgenius
from config import GENIUS_ACCESS_TOKEN, PROXIES
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Настройки для обхода блокировок
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


# Инициализация сессии с User-Agent и прокси
session = requests.Session()
session.headers.update(HEADERS)
if PROXIES:
    session.proxies.update(PROXIES)

# Инициализация Genius с кастомной сессией
genius = lyricsgenius.Genius(
    GENIUS_ACCESS_TOKEN, user_agent=session, timeout=15, retries=3
)


def get_lyrics_from_url(url: str):
    """Парсит текст песни по ссылке из Genius"""
    try:
        print("Парсим")
        response = session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find_all("div", {"data-lyrics-container": "true"})
        if container:
            trash = soup.find("div", {"data-exclude-from-selection": "true"})
            if trash:
                trash.decompose()
        if container:
            print("✅ Текст найден через URL")
            lyrics = ""
            for p in container:
                if p.get_text() == "":
                    continue
                lyrics += p.get_text(separator="\n").strip() + "\n"
            return lyrics
        else:
            print("❌ Текст не найден на странице")
            return None
    except Exception as e:
        print(f"❌ Ошибка парсинга по URL: {e}")
        return None


def get_lyrics_direct(song_name: str, artist_name: str):
    """Резервный метод: парсинг текста с сайта Genius"""
    try:
        # Поиск ссылки через Google
        query = quote_plus(f"{song_name} {artist_name} site:genius.com")
        search_url = f"https://www.google.com/search?q={query}"
        response = session.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Извлечение ссылки на песню
        genius_link = None
        for link in soup.find_all("a"):
            href = link.get("href")
            if "genius.com" in href and "/lyrics" in href:
                genius_link = href.split("/url?q=")[-1].split("&")[0]
                break

        if not genius_link:
            print(f"[Парсинг] Ссылка не найдена для {song_name} — {artist_name}")
            return None

        # Парсинг текста песни
        song_response = session.get(genius_link)
        song_soup = BeautifulSoup(song_response.text, "html.parser")
        lyrics_div = song_soup.find("div", {"data-lyrics-container": "true"})

        time.sleep(3)
        return lyrics_div.get_text(separator="\n").strip() if lyrics_div else None

    except Exception as e:
        print(f"[Парсинг] Ошибка при парсинге: {e}")
        return None


def get_lyrics_ovh(song_name: str, artist_name: str):
    """Альтернативный API: lyrics.ovh"""
    try:
        url = f"https://api.lyrics.ovh/v1/{quote_plus(artist_name)}/{quote_plus(song_name)}"
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            time.sleep(2)
            return data.get("lyrics")
        return None
    except Exception as e:
        print(f"[Lyrics.ovh] Ошибка: {e}")
        return None


def get_lyrics_safe(song_name: str, artist_name: str):
    """
    Возвращает текст песни через Genius API с резервными методами
    """
    try:
        time.sleep(3)  # Защита от частых запросов
        search_query = f"{song_name} {artist_name}"
        results = genius.search_songs(search_query)

        if not results or not results.get("hits"):
            print(f"❌ Ничего не найдено по запросу: {search_query}")
            return None

        # Поиск точного совпадения
        for hit in results["hits"]:
            song_data = hit["result"]
            if (
                song_name.lower() in song_data["title"].lower()
                and song_data["primary_artist"]["name"].lower() == artist_name.lower()
            ):

                song_id = song_data["id"]
                full_song = genius.song(song_id)
                url = full_song["song"]["url"]
                # Проверка наличия текста в API
                if full_song and full_song.get("lyrics"):
                    print("✅ Текст найден через Genius API")
                    print(full_song["lyrics"].strip())
                    return full_song["lyrics"].strip()

                # Если текста нет, но есть URL — парсим его

                elif full_song and url:
                    print("📎 Текст не найден напрямую, пробую парсинг по ссылке")
                    lyrics = get_lyrics_from_url(url)

                    if lyrics:
                        return lyrics
                    else:
                        print("❌ Не удалось получить текст по ссылке")

        print("⚠️ Текст не найден через Genius API, пробую резервные методы...")

        # Резервный метод 1: Парсинг сайта Genius
        direct_lyrics = get_lyrics_direct(song_name, artist_name)
        if direct_lyrics:
            print("✅ Текст найден через парсинг Genius")
            return direct_lyrics

        # Резервный метод 2: Использование lyrics.ovh
        ovh_lyrics = get_lyrics_ovh(song_name, artist_name)
        if ovh_lyrics:
            print("✅ Текст найден через lyrics.ovh")
            return ovh_lyrics

        print("❌ Все методы не смогли найти текст песни")
        return None

    except lyricsgenius.GeniusError as ge:
        print(f"❌ Genius API ошибка: {ge}")
        return get_lyrics_direct(song_name, artist_name) or get_lyrics_ovh(
            song_name, artist_name
        )

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return get_lyrics_direct(song_name, artist_name) or get_lyrics_ovh(
            song_name, artist_name
        )
