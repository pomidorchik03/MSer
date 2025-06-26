from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from spotify import get_track_info, get_artist_info, get_artist_albums, get_album_tracks
from genius import get_lyrics_safe
from tracks_list import info_type_keyboard
from artists import albums_keyboard, album_tracks_keyboard
from helpers import convert_ms_to_time
from background import check_for_new_releases
from fan_management import remove_favorite
from commands import show_help


router = Router()



@router.callback_query(lambda c: c.data.startswith("track_"))
async def process_track_choice(callback: types.CallbackQuery, state: FSMContext):
    '''Клавиатура с выбором информации и текстом'''
    track_id = callback.data.split("_")[-1]
    await callback.message.answer(
        "📌 Выберите тип информации:",
        reply_markup=info_type_keyboard(track_id).as_markup(),
    )
    await callback.answer()
    await state.clear()

@router.callback_query(lambda c: c.data.startswith("info_"))
async def show_track_info(callback: types.CallbackQuery):
    '''Информация о треке'''
    track_id = callback.data.split("_")[1]
    track = await get_track_info(track_id)

    text = f"""
            🎵 {track['name']}
            👨🎤 Исполнитель: {', '.join([a['name'] for a in track['artists']])}
            💽 Альбом: {track['album']['name']}
            ⏱ Длительность: {convert_ms_to_time(track['duration_ms'])}
            """
    await callback.message.answer(text)
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("lyrics_"))
async def show_lyrics(callback: types.CallbackQuery):
    '''Текст трека'''
    track_id = callback.data.split("_")[1]
    track = await get_track_info(track_id)

    try:
        name = track["name"]
        artist_name = track["artists"][0]["name"] if track["artists"] else "Unknown"

        lyrics = get_lyrics_safe(name, artist_name)
    
        if not lyrics:
            return await callback.message.answer("😕 Текст не найден")

        await callback.message.answer(
            f"📝 {name}:\n\n{lyrics[:3000]}", parse_mode="HTML"
        )
    except Exception as e:
        print(e)
        await callback.message.answer("⚠️ Ошибка при получении текста")
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("artist_"))
async def show_artist_info(callback: types.CallbackQuery):
    '''Информация о артисте'''
    artist_id = callback.data.split("_")[1]
    artist = await get_artist_info(artist_id)

    text = (
        f"🎤 {artist['name']}\n"
        f"🎭 Жанры: {', '.join(artist.get('genres', ['не указаны']))}\n"
        f"📈 Популярность: {artist['popularity']}/100\n"
        f"👥 Подписчики: {artist['followers']['total']:,}"
    )
    await callback.message.answer(text)

    albums = await get_artist_albums(artist_id)
    if albums and albums['items']:
        await callback.message.answer(
            "💿 Альбомы:",
            reply_markup=albums_keyboard(albums['items'])
        )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("album_"))
async def show_album_tracks(callback: types.CallbackQuery):
    '''Содержание трека'''
    album_id = callback.data.split("_")[1]
    album_tracks = await get_album_tracks(album_id)

    if not album_tracks or not album_tracks['items']:
        await callback.message.answer("⚠️ Альбом не содержит треков")
        return await callback.answer()

    await callback.message.answer(
        "🎧 Треки альбома:",
        reply_markup=album_tracks_keyboard(album_tracks['items'])
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "check_releases")
async def manual_check(callback: types.CallbackQuery):
    await callback.message.answer("🔄 Проверка новых релизов запущена...")
    await check_for_new_releases(callback.bot)
    await callback.answer()
    
@router.callback_query(lambda c: c.data.startswith("remove_"))
async def remove_favorite_callback(callback: types.CallbackQuery):
    '''Удаление подписки'''
    artist_id = callback.data.split("_")[1]
    user_id = str(callback.from_user.id)
    
    if remove_favorite(user_id, artist_id):
        await callback.message.answer("💔 Артист удален из избранного")
    else:
        await callback.message.answer("❌ Артист не найден в избранном")
    
    await callback.answer()
    
@router.callback_query(lambda c: c.data == "show_help")
async def show_help_callback(callback: types.CallbackQuery):
    '''Подсказка'''
    await show_help(callback.message)
    await callback.answer()