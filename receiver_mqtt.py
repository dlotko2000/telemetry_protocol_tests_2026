import json
import time

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883

DATA_TOPIC = "telemetry/data"
ACK_TOPIC = "telemetry/data/ack"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT receiver connected")
        client.subscribe(DATA_TOPIC)
        print(f"Subscribed to topic: {DATA_TOPIC}")
    else:
        print(f"Connection failed: {rc}")


def on_message(client, userdata, msg):
    server_receive_ts = time.time()

    artificial_delay_ms = 0
    message_id = None
    scenario_id = None
    run_number = None
    client_id = None
    payload_raw = msg.payload.decode("utf-8", errors="replace")

    try:
        payload = json.loads(payload_raw)
        message_id = payload.get("message_id")
        scenario_id = payload.get("scenario_id")
        run_number = payload.get("run_number")
        artificial_delay_ms = int(payload.get("artificial_delay_ms", 0))
        client_id = payload.get("client_id")
    except Exception:
        pass

    if artificial_delay_ms > 0:
        time.sleep(artificial_delay_ms / 1000.0)

    response = {
        "status": "received",
        "message_id": message_id,
        "scenario_id": scenario_id,
        "run_number": run_number,
        "server_receive_ts": server_receive_ts,
        "server_send_ts": time.time(),
        "payload_length": len(payload_raw.encode("utf-8")),
        "artificial_delay_ms": artificial_delay_ms,
        "client_id": client_id,
    }

    client.publish(ACK_TOPIC, json.dumps(response), qos=0)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  # type: ignore[attr-defined]
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker {BROKER_HOST}:{BROKER_PORT}")
    client.connect(BROKER_HOST, BROKER_PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()