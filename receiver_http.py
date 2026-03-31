import time
import json

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Telemetry HTTP Receiver")


class PayloadRequest(BaseModel):
    payload: str


@app.post("/telemetry")
def receive_telemetry(request: PayloadRequest):
    server_receive_ts = time.time()

    artificial_delay_ms = 0
    try:
        payload_json = json.loads(request.payload)
        artificial_delay_ms = int(payload_json.get("artificial_delay_ms", 0))
    except Exception:
        artificial_delay_ms = 0

    if artificial_delay_ms > 0:
        time.sleep(artificial_delay_ms / 1000.0)

    return {
        "status": "received",
        "server_receive_ts": server_receive_ts,
        "server_send_ts": time.time(),
        "payload_length": len(request.payload.encode("utf-8")),
        "artificial_delay_ms": artificial_delay_ms,
    }