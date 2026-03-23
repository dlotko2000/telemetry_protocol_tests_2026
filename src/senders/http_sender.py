import requests

from src.senders.base_sender import BaseSender


class HTTPSender(BaseSender):
    def __init__(self, host: str, port: int, endpoint: str) -> None:
        endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        self.url = f"http://{host}:{port}{endpoint}"
        self.session = requests.Session()

    def connect(self) -> None:
        # Dla HTTP połączenie jest bezstanowe, ale sesja już istnieje.
        pass

    def disconnect(self) -> None:
        self.session.close()

    def send_and_wait(self, payload: str, timeout_ms: int) -> dict:
        timeout_s = timeout_ms / 1000.0
        response = self.session.post(
            self.url,
            json={"payload": payload},
            timeout=timeout_s,
        )

        return {
            "status": "success" if response.ok else "error",
            "response_text": response.text,
            "response_size": len(response.text.encode("utf-8")),
            "http_status_code": response.status_code,
        }