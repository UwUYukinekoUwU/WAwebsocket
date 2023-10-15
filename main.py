
import websockets
import asyncio
import time

PORT = 8080
print("Server listening on Port " + str(PORT))

# A set of connected ws clients
connected = list()
banned_IPs = list()
client_id = 1


# The main behavior function for this server
async def echo(websocket, path):
    # don't let the exiled ones in
    client_ip = websocket.remote_address[0]
    if client_ip in banned_IPs:
        disconnect(websocket=websocket)

    print("A client just connected")
    # Store a copy of the connected client
    global client_id
    connected.append((client_id, websocket))
    client_id += 1
    # Handle incoming messages
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            # ban Rum
            if message == "Rum":
                await ban(websocket=websocket)
                return

            # get current sender's id to use as a name
            current_id = 0
            for clients in connected:
                if clients[1] == websocket:
                    current_id = clients[0]
                    break

            for conn in connected:
                print(f"sending to {conn[0]}")
                await conn[1].send(f"{current_id} said: {message}")

    # Handle disconnecting clients
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")
    finally:
        disconnect(websocket)


def disconnect(websocket):
    print("disconnected")
    for client in connected:
        if client[1] == websocket:
            connected.remove(client)


async def ban(websocket):
    print("banned")
    await websocket.send("SERVER_MESSAGE: Nuh uh.")
    banned_IPs.append(websocket.remote_address[0])
    disconnect(websocket)


if __name__ == "__main__":
    start_server = websockets.serve(echo, "localhost", PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()




