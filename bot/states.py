from aiogram.fsm.state import State, StatesGroup

class TrackSearch(StatesGroup):
    waiting_query = State()
    waiting_track_choice = State()

class ArtistSearch(StatesGroup):
    waiting_query = State()
    waiting_artist_choice = State()