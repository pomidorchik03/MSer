from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from spotify import get_artist_info


def get_main_keyboard():
    '''Главная клавиатура'''
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="🎵 Поиск треков"),
        types.KeyboardButton(text="🎙️ Поиск исполнителей")
    )
    builder.row(
        types.KeyboardButton(text="📆 Новые релизы"),
        types.KeyboardButton(text="❓ Справка")
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def artist_keyboard(artists):
    '''Клавиатура с артистами'''
    builder = InlineKeyboardBuilder()
    for idx, artist in enumerate(artists[:10], 1):
        builder.add(types.InlineKeyboardButton(
            text=f"{idx}. {artist['name']}",
            callback_data=f"artist_{artist['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def favorites_keyboard(favorites: dict):
    '''Клавиатура с подписками'''
    builder = InlineKeyboardBuilder()
    for artist_id in favorites:
        try:
            artist = get_artist_info(artist_id)
            builder.add(types.InlineKeyboardButton(
                text=f"❌ {artist['name']}",
                callback_data=f"remove_{artist_id}"
            ))
        except:
            continue
    builder.adjust(1)
    return builder.as_markup()

def albums_keyboard(albums):
    '''Клавиатура с альбомами'''
    builder = InlineKeyboardBuilder()
    for album in albums:
        release_year = album['release_date'][:4] if album['release_date'] else 'не указана'
        builder.add(types.InlineKeyboardButton(
            text=f"{album['name']} ({release_year})",
            callback_data=f"album_{album['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def album_tracks_keyboard(tracks):
    '''Клавиатура с треками в альбоме'''
    builder = InlineKeyboardBuilder()
    for idx, track in enumerate(tracks, 1):
        builder.add(types.InlineKeyboardButton(
            text=f"{idx}. {track['name']} — {', '.join([a['name'] for a in track['artists']])}",
            callback_data=f"track_album_{track['id']}"
        ))
    builder.adjust(1)
    return builder.as_markup()
