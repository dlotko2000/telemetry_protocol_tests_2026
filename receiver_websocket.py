import asyncio
import json
import time

import websockets
from websockets.exceptions import ConnectionClosed

HOST = "10.10.10.169"

async def handle_connection(websocket):
    try:
        async for message in websocket:
            print(message)

            server_receive_ts = time.time()

            artificial_delay_ms = 0
            message_id = None
            scenario_id = None
            run_number = None

            try:
                payload = json.loads(message)
                message_id = payload.get("message_id")
                scenario_id = payload.get("scenario_id")
                run_number = payload.get("run_number")
                artificial_delay_ms = int(payload.get("artificial_delay_ms", 0))
            except json.JSONDecodeError:
                pass

            if artificial_delay_ms > 0:
                await asyncio.sleep(artificial_delay_ms / 1000.0)

            response = {
                "status": "received",
                "message_id": message_id,
                "scenario_id": scenario_id,
                "run_number": run_number,
                "server_receive_ts": server_receive_ts,
                "server_send_ts": time.time(),
                "payload_length": len(message.encode("utf-8")),
                "artificial_delay_ms": artificial_delay_ms,
            }

            await websocket.send(json.dumps(response, ensure_ascii=False))

    except ConnectionClosed:
        print("client disconnected")


async def main():
    server = await websockets.serve(handle_connection, HOST, 8765)
    print(f"WebSocket receiver started on ws://{HOST}:8765/ws")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())