import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

waiting = []
pairs = {}

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("🤫 Анонимный чат\nНапиши /find")

@dp.message_handler(commands=['find'])
async def find(msg: types.Message):
    uid = msg.from_user.id
    if uid in waiting or uid in pairs:
        return

    if waiting:
        other = waiting.pop(0)
        pairs[uid] = other
        pairs[other] = uid
        await bot.send_message(uid, "✅ Собеседник найден")
        await bot.send_message(other, "✅ Собеседник найден")
    else:
        waiting.append(uid)
        await msg.answer("⏳ Ищем собеседника...")

@dp.message_handler(commands=['stop'])
async def stop(msg: types.Message):
    uid = msg.from_user.id
    if uid in pairs:
        other = pairs.pop(uid)
        pairs.pop(other, None)
        await bot.send_message(other, "❌ Собеседник вышел")
    waiting[:] = [u for u in waiting if u != uid]
    await msg.answer("Ты вышел из чата")

@dp.message_handler()
async def relay(msg: types.Message):
    uid = msg.from_user.id
    if uid in pairs:
        await bot.send_message(pairs[uid], msg.text)

if __name__ == "__main__":
    executor.start_polling(dp)
