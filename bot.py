from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import TELEGRAM_TOKEN
import asyncio
from track import track_search, convert_ms_to_time
from keyboards import tracks_keyboard, info_type_keyboard
from spotipy import Spotify
from spotify_client import sp 
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from genius_client import *

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Состояния для FSM
class TrackSearch(StatesGroup):
    waiting_query = State()
    waiting_track_choice = State()


# Главное меню
@dp.message(Command("start"))
async def start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="🎵 Поиск треков"),
        types.KeyboardButton(text="🎙️ Поиск исполнителей")
    )
    builder.row(types.KeyboardButton(text="📆 Новые релизы"))
    
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

# Обработчик кнопки "Поиск треков"
@dp.message(F.text == "🎵 Поиск треков")
async def search_tracks_handler(message: types.Message, state: FSMContext):
    await message.answer("🔍 Введите название трека:")
    await state.set_state(TrackSearch.waiting_query)

# Обработчик ввода названия трека
@dp.message(TrackSearch.waiting_query)
async def process_track_query(message: types.Message, state: FSMContext):
    try:
        # Ищем треки
        tracks = await track_search(message.text)
        
        if not tracks:
            await message.answer("😔 Ничего не найдено")
            await state.clear()
            return

        # Отправляем клавиатуру с результатами
        await message.answer(
            "🎧 Найденные треки:",
            reply_markup=tracks_keyboard(tracks).as_markup()
        )
        await state.set_state(TrackSearch.waiting_track_choice)
        await state.update_data(tracks=tracks)

    except Exception as e:
        await message.answer("⚠️ Ошибка при поиске")
        await state.clear()

# Обработчик выбора трека
@dp.callback_query(F.data.startswith("track_"), TrackSearch.waiting_track_choice)
async def process_track_choice(callback: types.CallbackQuery, state: FSMContext):
    track_id = callback.data.split("_")[1]
    await callback.message.answer(
        "📌 Выберите тип информации:",
        reply_markup=info_type_keyboard(track_id).as_markup()
    )
    await callback.answer()
    await state.clear()

# Обработчик информации о треке
@dp.callback_query(F.data.startswith("info_"))
async def show_track_info(callback: types.CallbackQuery):
    track_id = callback.data.split("_")[1]
    track = sp.track(track_id)
    
    text = (
        f"🎵 {track['name']}\n"
        f"👨🎤 Исполнитель: {', '.join([a['name'] for a in track['artists']])}\n"
        f"💽 Альбом: {track['album']['name']}\n"
        f"⏱ Длительность: {convert_ms_to_time(track["duration_ms"])}"
    )
    
    await callback.message.answer(text)
    await callback.answer()

# Обработчик текста песни
@dp.callback_query(F.data.startswith("lyrics_"))
async def show_lyrics(callback: types.CallbackQuery):
    track_id = callback.data.split("_")[1]
    track = sp.track(track_id)
    
    try:
        name = track['name']
        artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown"
        
        song = genius.search_song(name, artist_name)
        if not song or not song.lyrics:
            return await callback.message.answer("😕 Текст не найден")
        
        lyrics = song.lyrics.split('[', 1)
        cleaned_lyrics = ('[' + lyrics[1] if len(lyrics) > 1 else lyrics[0]).strip()
        
        await callback.message.answer(
            f"📝 {name}:\n\n{cleaned_lyrics[:3000]}...",
            parse_mode="HTML"
        )
        
    except:
        await callback.message.answer("⚠️ Ошибка при получении текста")    
    await callback.answer()

async def main():
    await dp.start_polling(bot)
    print("Бот включен")

if __name__ == "__main__":
    asyncio.run(main())