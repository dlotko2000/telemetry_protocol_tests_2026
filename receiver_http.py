import time

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Telemetry HTTP Receiver")


class PayloadRequest(BaseModel):
    payload: str


@app.post("/telemetry")
def receive_telemetry(request: PayloadRequest):
    now = time.time()
    return {
        "status": "received",
        "server_receive_ts": now,
        "payload_length": len(request.payload.encode("utf-8")),
    }