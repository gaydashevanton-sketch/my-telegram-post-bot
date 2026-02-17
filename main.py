import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types  # добавили types
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.channels import router as channels_router
from handlers.post_creation import router as post_router

logging.basicConfig(level=logging.INFO)

# Обработчик для пинга
async def ping_handler(request):
    return web.Response(text="OK")

# Функция запуска веб-сервера
async def run_web_server():
    port = int(os.getenv("PORT", "10000"))
    app = web.Application()
    app.router.add_get("/ping", ping_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server for pinging started on port {port}")
    await asyncio.Event().wait()  # держим сервер включённым

async def main():
    # Запускаем веб-сервер в фоне
    asyncio.create_task(run_web_server())

    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)
    dp.include_router(channels_router)
    dp.include_router(post_router)

    # ========== ВРЕМЕННЫЙ ОТЛАДОЧНЫЙ ХЕНДЛЕР ==========
    @dp.message()
    async def debug_handler(message: types.Message):
        print(f"🔥 Получено сообщение из чата: {message.chat.id} (тип: {type(message.chat.id)})")
        print(f"📢 Название чата: {message.chat.title}")
        # Не отвечаем, просто логируем
    # =================================================

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
