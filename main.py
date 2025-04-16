from dotenv import load_dotenv
load_dotenv()

import os
import requests
import asyncio
from flask import Flask, request, jsonify

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Flask app
app = Flask(__name__)

# aiogram setup
dp = Dispatcher()
chat_id = os.getenv('chat_id')  # ID пользователя или чата из .env
bot = Bot(token=os.getenv('token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# POST /send endpoint
@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(bot.send_message(chat_id=chat_id, text=message))
    return jsonify({'status': 'Message sent'}), 200


# Optional: background task
async def repeated_task(bot: Bot):
    while True:
        await asyncio.sleep(3600)
        # your periodic logic here

# Main entrypoint
async def main() -> None:
    asyncio.create_task(repeated_task(bot))
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Start Flask in a background thread
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

    # Start bot polling
    asyncio.run(main())
