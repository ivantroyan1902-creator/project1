#Импорт всех модулей
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from openai import AsyncClient
from telebot.apihelper import session

#Токены доступа
TOKEN = "8262980519:AAGdcSkpx9Q_KnLPnSNKWiAOURsWBYWLIbg"
AI_TOKEN = "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"
PROXY_URL = "http://pgvgvgdo:dcj271bl2r12@31.59.20.176:6754"

#Создание диспетчера
dp = Dispatcher()

#Асинхронная функция для генерации ответа нейросетью
async def generate_responce(prompt):
    client = AsyncClient(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    completion = await client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-chat",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


#Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, Добро пожаловать!\n"
                         f"Напишите любое сообщение в чат и оно будет обработано нейросетью!")


#Обработик всех сообщений
@dp.message()
async def echo_handler(message: Message) -> None:
   msg = await message.answer('Нейросеть генерирует ответ, подождите пожалуйста')
   response = await generate_responce(message.text)
   await msg.delete()
   await message.answer(f'{response}')

#Главная функция main
async def main() -> None:
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


#Точка входа
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())