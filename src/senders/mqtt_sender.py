import json
import threading
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

        # kompatybilność z paho-mqtt 2.x
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) # type: ignore[attr-defined]

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self._connected = False
        self._connect_event = threading.Event()

        self._pending_responses = {}

        self._pending_message_id: Optional[int] = None
        self._pending_response: Optional[dict] = None
        self._response_event = threading.Event()
        self._lock = threading.Lock()

    def connect(self) -> None:
        self.client.connect(self.host, self.port, keepalive=60)
        self.client.loop_start()

        if not self._connect_event.wait(timeout=5):
            raise ConnectionError("MQTT connection timeout")

        print("SUBSCRIBING TO ACK TOPIC:", self.ack_topic)
        self.client.subscribe(self.ack_topic, qos=self.qos)

    def disconnect(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def send_and_wait(self, payload: str, timeout_ms: int) -> dict:
        if not self._connected:
            raise ConnectionError("MQTT not connected")

        payload_json = json.loads(payload)
        message_id = payload_json.get("message_id")

        if message_id is None:
            raise ValueError("Payload must contain message_id")

        event = threading.Event()

        with self._lock:
            self._pending_responses[message_id] = {
                "event": event,
                "response": None
            }

        print(f"PUBLISHING message_id={message_id}")

        result = self.client.publish(self.publish_topic, payload, qos=self.qos)

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"Publish failed: {result.rc}")

        if not event.wait(timeout=timeout_ms / 1000):
            with self._lock:
                self._pending_responses.pop(message_id, None)
            raise TimeoutError(f"MQTT ACK timeout (msg_id={message_id})")

        with self._lock:
            data = self._pending_responses.pop(message_id)

        response = data["response"]

        response_text = json.dumps(response, ensure_ascii=False)

        return {
            "status": "success" if response.get("status") == "received" else "error",
            "response_text": response_text,
            "response_size": len(response_text.encode()),
            "http_status_code": None,
            "response_json": response,
    }

    # ---------- CALLBACKI ----------

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT sender connected")
            self._connected = True
            self._connect_event.set()
        else:
            print(f"MQTT connection failed: {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except Exception:
            return

        message_id = payload.get("message_id")

        print("ACK PARSED message_id:", message_id)

        if message_id is None:
            return

        with self._lock:
            entry = self._pending_responses.get(message_id)

            if entry:
                entry["response"] = payload
                entry["event"].set()