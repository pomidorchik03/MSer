from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states import TrackSearch
from spotify import track_search as search_tracks
from tracks_list import tracks_keyboard

router = Router()

@router.message(lambda m: m.text == "🎵 Поиск треков")
async def search_tracks_handler(message: types.Message, state: FSMContext):
    '''Обработчик текстового ввода (🎵 Поиск треков)'''
    await message.answer("🔍 Введите название трека или отрывок этого трека:")
    await state.set_state(TrackSearch.waiting_query)

@router.message(TrackSearch.waiting_query)
async def process_track_query(message: types.Message, state: FSMContext):
    '''Вывод результата'''
    tracks = await search_tracks(message.text)
    
    if not tracks:
        await message.answer("😔 Ничего не найдено")
        return await state.clear()

    await message.answer(
        "🎧 Найденные треки:",
        reply_markup=tracks_keyboard(tracks).as_markup()
    )
    await state.update_data(tracks=tracks)
    await state.set_state(TrackSearch.waiting_track_choice)
