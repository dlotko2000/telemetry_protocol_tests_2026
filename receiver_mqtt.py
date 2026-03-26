import json
import time

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883

DATA_TOPIC = "telemetry/data"
ACK_TOPIC = f"{DATA_TOPIC}/ack"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT receiver connected")
        client.subscribe(DATA_TOPIC)
        print(f"Subscribed to topic: {DATA_TOPIC}")
    else:
        print(f"Connection failed: {rc}")


def on_message(client, userdata, msg):
    print("RAW RECEIVED:", msg.topic, msg.payload.decode("utf-8", errors="replace"))
    server_receive_ts = time.time()

    try:
        payload = json.loads(msg.payload.decode())
        message_id = payload.get("message_id")
        scenario_id = payload.get("scenario_id")
        run_number = payload.get("run_number")
        print(f"PARSED message_id={message_id}, scenario_id={scenario_id}, run_number={run_number}")
    except Exception as e:
        print("JSON ERROR:", e)
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
    }

    print("SENDING ACK TO:", ACK_TOPIC, response)
    client.publish(ACK_TOPIC, json.dumps(response), qos=0)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker {BROKER_HOST}:{BROKER_PORT}")
    client.connect(BROKER_HOST, BROKER_PORT)

    client.loop_forever()


if __name__ == "__main__":
    main()