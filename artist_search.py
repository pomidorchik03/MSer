from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states import ArtistSearch
from spotify import artist_search
from artists import artist_keyboard

router = Router()

@router.message(lambda m: m.text == "🎙️ Поиск исполнителей")
async def search_artists_handler(message: types.Message, state: FSMContext):
    '''Обработчик текстового ввода(🎙️ Поиск исполнителей)'''
    await message.answer("🔍 Введите имя исполнителя:")
    await state.set_state(ArtistSearch.waiting_query)

@router.message(ArtistSearch.waiting_query)
async def process_artist_query(message: types.Message, state: FSMContext):
    '''Вывод результата'''
    artists = await artist_search(message.text)
    
    if not artists:
        await message.answer("😔 Ничего не найдено")
        return await state.clear()

    await message.answer(
        "🎤 Найденные исполнители:",
        reply_markup=artist_keyboard(artists)
    )
    await state.update_data(artists=artists)
    await state.set_state(ArtistSearch.waiting_artist_choice)