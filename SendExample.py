import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://127.0.0.1:55356/ws/announce/" #defines the websocket
    message = json.dumps({"message": input("What is your message?: ")}) #gets the message
    async with websockets.connect(uri) as websocket: #waits until it connects with the websocket
        await websocket.send(message) # sends the message
        print(f"Sent: {message}")

while True:
    asyncio.run(websocket_client())