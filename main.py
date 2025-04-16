from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn

# Mongo setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/agrodb")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.get_default_database()
blacklist = db.blacklist

# Telegram bot
bot = Bot(
    token=os.getenv("token"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
chat_id = os.getenv("chat_id")

from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI()
# Дозволяємо CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # або вкажи ['http://localhost:8080'] для безпеки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message")
    client_ip = request.client.host

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # check if IP in blacklist
    if await blacklist.find_one({"ip": client_ip}):
        raise HTTPException(status_code=403, detail="IP is blocked")

    try:
        # create inline keyboard
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🚫 Block", callback_data=f"block:{client_ip}")]
            ]
        )

        await bot.send_message(
            chat_id=chat_id,
            text=f"<b>New message:</b>\n\n{message}\n\nIP: <code>{client_ip}</code>",
            reply_markup=keyboard
        )
        return {"status": "Message sent", "ip": client_ip}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Handle button click
@dp.callback_query(lambda c: c.data.startswith("block:"))
async def block_ip(callback: CallbackQuery):
    ip_to_block = callback.data.split(":")[1]
    if not await blacklist.find_one({"ip": ip_to_block}):
        await blacklist.insert_one({"ip": ip_to_block})
        await callback.message.answer(f"✅ IP <code>{ip_to_block}</code> added to blacklist.")
    else:
        await callback.message.answer(f"⚠️ IP <code>{ip_to_block}</code> already in blacklist.")

    await callback.answer("Blocked!")


# Background task (optional)
async def repeated_task():
    while True:
        await asyncio.sleep(3600)
        # Your logic here


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(repeated_task())
    asyncio.create_task(dp.start_polling(bot))


# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
