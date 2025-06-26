import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from background import check_for_new_releases


from spotify import init_spotify
sp = init_spotify()


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


from commands import router as commands_router
from track_search import router as track_search_router
from artist_search import router as artist_search_router
from callbacks import router as callbacks_router

dp.include_router(commands_router)
dp.include_router(track_search_router)
dp.include_router(artist_search_router)
dp.include_router(callbacks_router)


async def run_background_check(bot):
    await check_for_new_releases(bot)

async def main():
    asyncio.create_task(run_background_check(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())