import asyncio
import json
import time

import websockets
from websockets.exceptions import ConnectionClosed


async def handle_connection(websocket):
    print("connection handler called")

    try:
        async for message in websocket:
            server_receive_ts = time.time()

            try:
                payload = json.loads(message)
                message_id = payload.get("message_id")
                scenario_id = payload.get("scenario_id")
                run_number = payload.get("run_number")
            except json.JSONDecodeError:
                message_id = None
                scenario_id = None
                run_number = None

            response = {
                "status": "received",
                "message_id": message_id,
                "scenario_id": scenario_id,
                "run_number": run_number,
                "server_receive_ts": server_receive_ts,
                "server_send_ts": time.time(),
                "payload_length": len(message.encode("utf-8")),
            }

            await websocket.send(json.dumps(response, ensure_ascii=False))

    except ConnectionClosed:
        print("client disconnected")


async def main():
    server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
    print("WebSocket receiver started on ws://0.0.0.0:8765/ws")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())