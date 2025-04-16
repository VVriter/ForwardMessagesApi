from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
import uvicorn

# BOT SETUP
bot = Bot(
    token=os.getenv("token"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
chat_id = os.getenv("chat_id")

# FASTAPI APP
app = FastAPI()

@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    try:
        await bot.send_message(chat_id=chat_id, text=message)
        return {"status": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Background task (optional)
async def repeated_task():
    while True:
        await asyncio.sleep(3600)
        # Your logic here


# Startup event to launch the bot polling & background task
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(repeated_task())
    asyncio.create_task(dp.start_polling(bot))


# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
