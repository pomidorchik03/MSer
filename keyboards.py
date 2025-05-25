from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from typing import List

def tracks_keyboard(tracks: List[dict]) -> InlineKeyboardBuilder:
    """Клавиатура с найденными треками"""
    builder = InlineKeyboardBuilder()
    for track in tracks:
            button_text = (
                f"{track['name'][:15]} - " 
                f"{track['artists'][:15]} "
                f"({track['duration']})"
            )
            
            builder.add(InlineKeyboardButton(
                text=button_text,
                callback_data=f"track_{track['id']}"
            ))
        
    builder.adjust(1)  
    return builder

def info_type_keyboard(track_id: str) -> InlineKeyboardBuilder:
    """Клавиатура выбора типа информации"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="ℹ️ Информация",
            callback_data=f"info_{track_id}"
        ),
        InlineKeyboardButton(
            text="📝 Текст песни",
            callback_data=f"lyrics_{track_id}"
        )
    )
    builder.adjust(2)
    return builder