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


## Launching the tool needed for HTML testing

 ```CMD
uvicorn receiver_http:app --host 0.0.0.0 --port 8000
```

## Launching the tool needed for Websocket testing

 ```CMD
python receiver_websocket.py
```
