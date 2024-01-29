from addemotionmarkup import add_emotion_markups, load_pkl_files
import websockets
import warnings
import asyncio
import configs
import json

warnings.filterwarnings('ignore')

async def producer(queue, request):
    print("Inserting request in queue..")
    await queue.put(request)

async def consumer(queue, websocket):
    while not queue.empty():
        request = await queue.get()
        print("Processing the request.")
        response_message = add_emotion_markups(request)
        print("Processed the request.")
        try:
            await websocket.send(json.dumps(response_message))
            print("Response sent to the client")
            queue.task_done()
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected before response could be sent.")

async def response(websocket, path):
    try:
        queue =asyncio.Queue()
        print("\nA client just connected.")
        response_message = load_pkl_files()
        await websocket.send(json.dumps(response_message))
        print("Initialization Completed.")

        while True: 
            request = await websocket.recv()
            print("Request received")
            request = json.loads(request)

            producer_task = asyncio.create_task(producer(queue, request))
            consumer_task = asyncio.create_task(consumer(queue, websocket))

            if request['message_id'] == 'add_emotion_markups':
                await asyncio.gather(producer_task, consumer_task)

    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected.", e)

start_server = websockets.serve(response, configs.ip, configs.port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
