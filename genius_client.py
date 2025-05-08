import lyricsgenius
from config import GENIUS_ACCESS_TOKEN

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=10)