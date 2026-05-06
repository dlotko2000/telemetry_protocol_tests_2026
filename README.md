# Short Descripton
The project was created to analyze MQTT vs. http/websocket communication, which was necessary to write a student thesis 

# CLI commands

## Testing HTTP communicationRunning a script based on a scenario 
*(HTML communication example)*

 ```CMD
python main.py run --scenario config/scenarios/scenario_http_basic.json
```

*(WebSocket communication example)*

 ```CMD
python main.py run --scenario config/scenarios/scenario_websocket_basic.json
```

*(MQTT communication example)*
```CMD
python main.py run --scenario config/scenarios/scenario_mqtt_basic.json      
```


## Launching the tool needed for HTML testing

 ```CMD
uvicorn receiver_http:app --host 0.0.0.0 --port 8000
```

## Launching the tool needed for Websocket testing

 ```CMD
python receiver_websocket.py
```

## Launching the tool needed for MQTT testing

```CMD
python receiver_mqtt.py
```

Docker command for runnig MOSQUITTO: 
```Docker
docker run -d -p 1883:1883 eclipse-mosquitto
```
## Launching all test script 


```
python main.py run --scenario config/scenarios/s1_http.json
python main.py run --scenario config/scenarios/s1_mqtt_qos0.json
python main.py run --scenario config/scenarios/s1_mqtt_qos1.json
python main.py run --scenario config/scenarios/s1_mqtt_qos2.json
python main.py run --scenario config/scenarios/s1_websocket.json
python main.py run --scenario config/scenarios/s2_http.json
python main.py run --scenario config/scenarios/s2_mqtt_qos0.json
python main.py run --scenario config/scenarios/s2_mqtt_qos1.json
python main.py run --scenario config/scenarios/s2_mqtt_qos2.json
python main.py run --scenario config/scenarios/s2_websocket.json
python main.py run --scenario config/scenarios/s3_http.json
python main.py run --scenario config/scenarios/s3_mqtt_qos0.json
python main.py run --scenario config/scenarios/s3_mqtt_qos1.json
python main.py run --scenario config/scenarios/s3_mqtt_qos2.json
python main.py run --scenario config/scenarios/s3_websocket.json
python main.py run --scenario config/scenarios/s4_http_1024b.json
python main.py run --scenario config/scenarios/s4_http_131072b.json
python main.py run --scenario config/scenarios/s4_http_16384b.json
python main.py run --scenario config/scenarios/s4_http_256b.json
python main.py run --scenario config/scenarios/s4_http_262144b.json
python main.py run --scenario config/scenarios/s4_http_32768b.json
python main.py run --scenario config/scenarios/s4_http_32b.json
python main.py run --scenario config/scenarios/s4_http_4096b.json
python main.py run --scenario config/scenarios/s4_http_65536b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_1024b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_131072.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_16384b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_256b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_262144b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_32768.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_32b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_4096b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos0_65536b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_1024b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_131072.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_16384b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_256b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_262144b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_32768.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_32b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_4096b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos1_65536b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_1024b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_131072.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_16384b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_256b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_262144b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_32768.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_32b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_4096b.json
python main.py run --scenario config/scenarios/s4_mqtt_qos2_65536b.json
python main.py run --scenario config/scenarios/s4_websocket_1024b.json
python main.py run --scenario config/scenarios/s4_websocket_131072.json
python main.py run --scenario config/scenarios/s4_websocket_16384b.json
python main.py run --scenario config/scenarios/s4_websocket_256b.json
python main.py run --scenario config/scenarios/s4_websocket_262144.json
python main.py run --scenario config/scenarios/s4_websocket_32768.json
python main.py run --scenario config/scenarios/s4_websocket_32b.json
python main.py run --scenario config/scenarios/s4_websocket_4096b.json
python main.py run --scenario config/scenarios/s4_websocket_65536b.json
python main.py run --scenario config/scenarios/s5_http.json
python main.py run --scenario config/scenarios/s5_mqtt_qos0.json
python main.py run --scenario config/scenarios/s5_mqtt_qos1.json
python main.py run --scenario config/scenarios/s5_mqtt_qos2.json
python main.py run --scenario config/scenarios/s5_websocket.json
python main.py run --scenario config/scenarios/s6_http_1000ms.json
python main.py run --scenario config/scenarios/s6_http_100ms.json
python main.py run --scenario config/scenarios/s6_http_250ms.json
python main.py run --scenario config/scenarios/s6_http_500ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos0_1000ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos0_100ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos0_250ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos0_500ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos1_1000ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos1_100ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos1_250ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos1_500ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos2_1000ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos2_100ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos2_250ms.json
python main.py run --scenario config/scenarios/s6_mqtt_qos2_500ms.json
python main.py run --scenario config/scenarios/s6_websocket_1000ms.json
python main.py run --scenario config/scenarios/s6_websocket_100ms.json
python main.py run --scenario config/scenarios/s6_websocket_250ms.json
python main.py run --scenario config/scenarios/s6_websocket_500ms.json
python main.py run --scenario config/scenarios/scenario_doc.md
python main.py run --scenario config/scenarios/scenario_http_basic.json
python main.py run --scenario config/scenarios/scenario_mqtt_basic.json
python main.py run --scenario config/scenarios/scenario_websocket_basic.json


python main.py run --scenario config/scenarios/s7_cli5_http.json
python main.py run --scenario config/scenarios/s7_cli5_mqtt_qos0.json
python main.py run --scenario config/scenarios/s7_cli5_mqtt_qos1.json
python main.py run --scenario config/scenarios/s7_cli5_mqtt_qos2.json
python main.py run --scenario config/scenarios/s7_cli5_websocket.json
python main.py run --scenario config/scenarios/s7_cli10_http.json
python main.py run --scenario config/scenarios/s7_cli10_mqtt_qos0.json
python main.py run --scenario config/scenarios/s7_cli10_mqtt_qos1.json
python main.py run --scenario config/scenarios/s7_cli10_mqtt_qos2.json
python main.py run --scenario config/scenarios/s7_cli10_websocket.json
python main.py run --scenario config/scenarios/s7_cli20_http.json
python main.py run --scenario config/scenarios/s7_cli20_mqtt_qos0.json
python main.py run --scenario config/scenarios/s7_cli20_mqtt_qos1.json
python main.py run --scenario config/scenarios/s7_cli20_mqtt_qos2.json
python main.py run --scenario config/scenarios/s7_cli20_websocket.json

```