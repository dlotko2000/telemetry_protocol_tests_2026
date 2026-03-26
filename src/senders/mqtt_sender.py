import json
import threading
import time
from typing import Optional

import paho.mqtt.client as mqtt

from src.senders.base_sender import BaseSender


class MQTTSender(BaseSender):
    def __init__(self, host: str, port: int, topic: str, qos: int = 0) -> None:
        self.host = host
        self.port = port
        self.publish_topic = topic
        self.ack_topic = f"{topic}/ack"
        self.qos = qos

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self._connected = False
        self._connect_event = threading.Event()

        self._pending_message_id: Optional[int] = None
        self._pending_response: Optional[dict] = None
        self._response_event = threading.Event()
        self._lock = threading.Lock()

    def connect(self) -> None:
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()

        connected = self._connect_event.wait(timeout=5.0)
        if not connected:
            raise ConnectionError("MQTT connection timeout")

        self.client.subscribe(self.ack_topic, qos=self.qos)

    def disconnect(self) -> None:
        try:
            self.client.loop_stop()
        finally:
            self.client.disconnect()
            self._connected = False
            self._connect_event.clear()

    def send_and_wait(self, payload: str, timeout_ms: int) -> dict:
        if not self._connected:
            raise ConnectionError("MQTT connection is not established")

        try:
            payload_json = json.loads(payload)
            message_id = payload_json.get("message_id")
        except json.JSONDecodeError as e:
            raise ValueError(f"MQTT payload must be valid JSON: {e}") from e

        if message_id is None:
            raise ValueError("MQTT payload does not contain 'message_id'")

        with self._lock:
            self._pending_message_id = message_id
            self._pending_response = None
            self._response_event.clear()

            result = self.client.publish(self.publish_topic, payload, qos=self.qos)
            result.wait_for_publish()

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"MQTT publish failed with code: {result.rc}")

            timeout_s = timeout_ms / 1000.0
            received = self._response_event.wait(timeout=timeout_s)

            if not received:
                raise TimeoutError(f"MQTT ACK timeout for message_id={message_id}")

            response = self._pending_response
            if response is None:
                raise RuntimeError("MQTT ACK event set but response is empty")

            response_text = json.dumps(response, ensure_ascii=False)

            return {
                "status": "success" if response.get("status") == "received" else "error",
                "response_text": response_text,
                "response_size": len(response_text.encode("utf-8")),
                "http_status_code": None,
                "response_json": response,
            }

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            self._connect_event.set()

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except Exception:
            return

        message_id = payload.get("message_id")
        if message_id is None:
            return

        with self._lock:
            if self._pending_message_id == message_id:
                self._pending_response = payload
                self._response_event.set()