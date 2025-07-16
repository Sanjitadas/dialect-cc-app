# ✅ main.py — FastAPI backend with WebSocket support
# ✅ main.py — FastAPI backend with WebSocket support

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, uuid
import asyncio
from utils.translator import smart_translate

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_users = {}  # user_id: {"lang": str, "ws": WebSocket}

@app.post("/connect_user")
async def connect_user(request: Request):
    user_id = request.query_params.get("user_id", str(uuid.uuid4()))
    lang = request.query_params.get("language", "en")
    connected_users[user_id] = {"lang": lang, "ws": None}
    return {"status": "connected", "user_id": user_id, "language": lang}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    if user_id not in connected_users:
        await websocket.close()
        return

    connected_users[user_id]["ws"] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            # Format: user_id::message::lang
            if "::" in data:
                sender, msg, lang = data.split("::", 2)
                responses = []
                for uid, user in connected_users.items():
                    target_lang = user["lang"]
                    translated = await smart_translate(msg, source_lang=lang, target_lang=target_lang)
                    responses.append({"user": sender, "translated": translated})
                for uid, user in connected_users.items():
                    if user["ws"]:
                        await user["ws"].send_json({"subtitles": responses})
    except WebSocketDisconnect:
        connected_users.pop(user_id, None)
    except Exception as e:
        print(f"WebSocket error: {e}")
        connected_users.pop(user_id, None)




