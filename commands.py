from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from spotify import find_artist_by_name
from fan_management import add_favorites, remove_favorite, load_fans_data, clear_news_for_user
from spotify import sp, get_artist_info
from artists import artist_keyboard


router = Router()

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="🎵 Поиск треков"),
        types.KeyboardButton(text="🎙️ Поиск исполнителей"),
    )
    builder.row(types.KeyboardButton(text="📆 Новые релизы"))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

@router.message(Command("remove"))
async def remove_favorite_handler(message: types.Message):
    artist_names = message.text.replace("/remove", "").strip().split(",")
    user_id = str(message.from_user.id)
    
    removed_artists = []
    for name in artist_names:
        name = name.strip()
        artist_id = await find_artist_by_name(name)
        if artist_id and remove_favorite(user_id, artist_id):
            removed_artists.append(name)
    
    if removed_artists:
        await message.answer(f"💔 Удалены: {', '.join(removed_artists)}")
    else:
        await message.answer("❌ Ничего не удалено — артист не найден в избранных")

@router.message(Command("myfavorites"))
async def show_favorites(message: types.Message):
    user_id = str(message.from_user.id)
    news = load_fans_data()
    
    if user_id not in news or not news[user_id]:
        await message.answer("📅 У вас пока нет новых релизов")
        return
    
    artist_ids = news[user_id]
    artists = []
    
    for artist_id in artist_ids:
        try:
            artist = await get_artist_info(artist_id)
            artists.append(artist)
        except Exception as e:
            print(f"Ошибка получения данных артиста {artist_id}: {e}")
    
    if not artists:
        await message.answer("❌ Артисты не найдены")
        return

    await message.answer(
        "🆕 Артисты со свежими релизами:",
        reply_markup=artist_keyboard(artists)
    )
    
    # Очистка уведомлений после просмотра
    clear_news_for_user(user_id)

@router.message(Command("favorites"))
async def add_favorites_handler(message: types.Message):
    artist_names = message.text.replace("/favorites", "").strip().split(",")
    user_id = str(message.from_user.id)
    
    added_artists = []
    for name in artist_names:
        name = name.strip()
        artist_id = await find_artist_by_name(name)
        if artist_id:
            added_artists.append(name)
            add_favorites(user_id, [artist_id])
    
    if added_artists:
        await message.answer(f"✅ Добавлены: {', '.join(added_artists)}")
    else:
        await message.answer("❌ Ничего не добавлено")

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_main_keyboard())