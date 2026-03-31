# Zestaw scenariuszy JSON

Folder zawiera:
- 18 podstawowych plików: scenariusze 1-6 dla HTTP, WebSocket i MQTT
- dodatkowe warianty dla scenariusza 4 (różne rozmiary payloadu)
- dodatkowe warianty dla scenariusza 6 (różne sztuczne opóźnienia)

## Założenia domyślne
- host: 127.0.0.1
- HTTP: port 8000, endpoint /telemetry
- WebSocket: port 8765, ścieżka /ws
- MQTT: port 1883, topic telemetry/data, qos = 1
- repetitions: 3
- payload_type: json
- concurrent_clients: 1

## Uwagi
1. Scenariusz 4 w wersjach podstawowych używa rozmiaru 1024 B.
2. Dodatkowe pliki `s4_*_*b.json` pozwalają od razu badać 32 B, 256 B, 1024 B, 4096 B i 16384 B.
3. Scenariusz 6 w wersjach podstawowych używa opóźnienia 250 ms.
4. Dodatkowe pliki `s6_*_*ms.json` pozwalają od razu badać 100 ms, 250 ms, 500 ms i 1000 ms.
5. W razie potrzeby można łatwo zmienić host, porty, endpointy albo timeout.