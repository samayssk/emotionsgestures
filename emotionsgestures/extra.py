import asyncio
import websockets
import json
 
# Set a new event loop
asyncio.set_event_loop(asyncio.new_event_loop())
 
# Create a set to store connected clients
connected_clients = set()
 
# Define a function to handle incoming client connections
async def handle_client(websocket, path):
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")
 
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message from client: {message}")
 
            # Read data from text file and send it to client
            with open('data.txt', 'r') as file:
                data = file.read()
            await websocket.send(data)
 
    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
        print(f"Client disconnected: {websocket.remote_address}")
        connected_clients.remove(websocket)
 
# Define a function to start the server
async def start_server():
    port = int(input("Enter the port number to start the server: "))
 
    start_server = websockets.serve(handle_client, 'localhost', port)
    print(f"Server started on port {port}")
 
    config = {
        "port": port
    }
 
    with open('config.json', 'w') as file:
        json.dump(config, file)
 
    await start_server
 
# Run the server
asyncio.get_event_loop().run_until_complete(start_server())
asyncio.get_event_loop().run_forever()