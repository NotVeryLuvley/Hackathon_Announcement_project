import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    message = json.dumps({"title": input("What is the title?: "), "desc": input("What is the description?: "), "tag": input("What is the tag?: "), "origin": input("What type of message is this?: ")}) #change the input date to a way to get the date from the os on android
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket
        await websocket.send(message) # sends the message
        print(f"Sent: {message}")

while True:
    asyncio.run(websocket_client())