from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from spotify import find_artist_by_name
from fan_management import add_favorites, remove_favorite, load_fans_data, clear_news_for_user
from spotify import sp, get_artist_info
from artists import artist_keyboard
from config import CHANELL_TOKEN

router = Router()

def get_main_keyboard():
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
            add_favorites(user_id, [artist_id])
            added_artists.append(name)
            
    
    if added_artists:
        await message.answer(f"✅ Добавлены: {', '.join(added_artists)}")
    else:
        await message.answer("❌ Ничего не добавлено")
        
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎵 Добро пожаловать в музыкального бота!\n\n"
        "Доступные команды:\n"
        "/favorites [артист 1, артист 2] — добавить любимых артистов\n"
        "/myfavorites — посмотреть список избранных артистов\n"
        "/remove [артист 1, артист 2] — удалить артиста из избранного\n"
        "/help — показать все команды\n\n"
        "Кнопки ниже позволяют:\n"
        "🎵 Поиск треков\n"
        "🎙️ Поиск исполнителей\n"
        "📆 Новые релизы — смотреть артистов с новыми альбомами\n"
        "❓ Справка — показывает список команд\n",
        reply_markup=get_main_keyboard()
    )        

@router.message(Command("help"))
async def show_help(message: types.Message):
    await message.answer(
        "📚 Список доступных команд:\n\n"
        "/start — перезапуск бота\n"
        "/favorites [артист 1, артист 2] — добавить артистов в избранное\n"
        "/myfavorites — посмотреть своих любимых артистов\n"
        "/remove [артист 1, артист 2] — удалить артистов из избранного\n"
        "/help — показать это сообщение\n\n"
        "Кнопки:\n"
        "🎵 Поиск треков — ищет песни\n"
        "🎙️ Поиск исполнителей — ищет артистов\n"
        "📆 Новые релизы — показывает артистов с новыми альбомами\n"
        "❓ Справка — показывает список команд"
    )
    
@router.message(lambda m: m.text == "❓ Справка")
async def show_help_button(message: types.Message):
    await show_help(message)
    
LAST_CHANNEL_POST = None

@router.channel_post()
async def handle_channel_post(post: types.Message):
    global LAST_CHANNEL_POST
    LAST_CHANNEL_POST = post

@router.message(lambda m: m.text == "📆 Новые релизы")
async def show_latest_release(message: types.Message):
    global LAST_CHANNEL_POST
    try:
        if LAST_CHANNEL_POST:
            await LAST_CHANNEL_POST.copy_to(chat_id=message.chat.id)
        else:
            await message.answer("❌ Новых постов пока нет")
    except Exception as e:
        print(f"Ошибка копирования поста: {e}")
        await message.answer("⚠️ Произошла ошибка")