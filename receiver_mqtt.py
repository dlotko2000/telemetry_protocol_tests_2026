import json
import time

import paho.mqtt.client as mqtt


BROKER_HOST = "0.0.0.0"
BROKER_PORT = 1883

DATA_TOPIC = "telemetry/data"
ACK_TOPIC = f"{DATA_TOPIC}/ack"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT receiver connected to broker")
        client.subscribe(DATA_TOPIC)
        print(f"Subscribed to topic: {DATA_TOPIC}")
    else:
        print(f"MQTT receiver connection failed, rc={rc}")


def on_message(client, userdata, msg):
    server_receive_ts = time.time()

    try:
        payload_raw = msg.payload.decode("utf-8")
        payload = json.loads(payload_raw)

        message_id = payload.get("message_id")
        scenario_id = payload.get("scenario_id")
        run_number = payload.get("run_number")
    except Exception:
        message_id = None
        scenario_id = None
        run_number = None
        payload_raw = msg.payload.decode("utf-8", errors="replace")

    response = {
        "status": "received",
        "message_id": message_id,
        "scenario_id": scenario_id,
        "run_number": run_number,
        "server_receive_ts": server_receive_ts,
        "server_send_ts": time.time(),
        "payload_length": len(payload_raw.encode("utf-8")),
    }

    client.publish(ACK_TOPIC, json.dumps(response, ensure_ascii=False), qos=0)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Uwaga: receiver nie jest brokerem.
    # Musi łączyć się do działającego brokera MQTT, np. Mosquitto.
    broker_host = "127.0.0.1"
    broker_port = 1883

    print(f"Connecting to MQTT broker at {broker_host}:{broker_port} ...")
    client.connect(broker_host, broker_port, keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    main()