import json
from typing import Optional

import websocket

from src.senders.base_sender import BaseSender


class WebSocketSender(BaseSender):
    def __init__(self, host: str, port: int, endpoint: str) -> None:
        endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        self.url = f"ws://{host}:{port}{endpoint}"
        self.connection: Optional[websocket.WebSocket] = None

    def connect(self) -> None:
        self.connection = websocket.create_connection(self.url)

    def disconnect(self) -> None:
        if self.connection is not None:
            try:
                self.connection.close()
            finally:
                self.connection = None

    def send_and_wait(self, payload: str, timeout_ms: int) -> dict:
        if self.connection is None:
            raise ConnectionError("WebSocket connection is not established")

        timeout_s = timeout_ms / 1000.0
        self.connection.settimeout(timeout_s)

        self.connection.send(payload)
        response_text = self.connection.recv()

        try:
            response_json = json.loads(response_text)
            status = "success" if response_json.get("status") == "received" else "error"
        except json.JSONDecodeError:
            response_json = None
            status = "success"

        return {
            "status": status,
            "response_text": response_text,
            "response_size": len(response_text.encode("utf-8")),
            "http_status_code": None,
            "response_json": response_json,
        }