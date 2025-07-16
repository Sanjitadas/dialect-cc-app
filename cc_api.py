# cc_api.py

# cc_api.py — Optional live audio-to-subtitle bridge (e.g., from Webex/Teams bots)

import asyncio
import websockets
import json

async def send_subtitle(user_id: str, message: str, lang: str, ws_url: str):
    uri = f"{ws_url}/{user_id}"
    try:
        async with websockets.connect(uri) as ws:
            await ws.send(f"{user_id}::{message}::{lang}")
    except Exception as e:
        print(f"❌ Subtitle push failed: {e}")









