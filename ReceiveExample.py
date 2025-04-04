import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket

        response = json.loads(await websocket.recv()) #waits until it gets a message from the server
        print(response)
        print(f"Title: {response['title']}")
        print(f"Description: {response['desc']}")
        print(f"Date: {response['date']}")
        print(f"Tag: {response['tag']}")
        print(f"Msgtype: {response['msgtype']}")

while True:
    asyncio.run(websocket_client())