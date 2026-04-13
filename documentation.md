# Dokumentacja systemu testowego do analizy protokołów komunikacyjnych

## 1. Wprowadzenie

System testowy został zaprojektowany w celu przeprowadzenia eksperymentalnej analizy wydajności oraz niezawodności protokołów komunikacyjnych wykorzystywanych w systemach IoT, w szczególności:

* HTTP
* WebSocket
* MQTT

System umożliwia realizację zdefiniowanych scenariuszy testowych, pomiar parametrów transmisji oraz zapis wyników do dalszej analizy.

---

## 2. Architektura systemu

System oparty jest o architekturę typu **klient–serwer**.

### Elementy systemu:

* **Sender (klient)** – generuje i wysyła wiadomości
* **Receiver (serwer)** – odbiera wiadomości i odsyła odpowiedzi
* **Broker MQTT** – pośrednik komunikacyjny dla MQTT
* **TestRunner** – orchestrator testów
* **MetricsCollector** – zbiera wyniki
* **SystemMonitor** – monitoruje zasoby systemowe

---

## 3. Struktura projektu

```text
src/
├── core/
│   ├── scenario.py
│   ├── test_runner.py
│   ├── payload_generator.py
│   ├── metrics_collector.py
│   ├── system_monitor.py
│   └── result_models.py
│
├── senders/
│   ├── base_sender.py
│   ├── http_sender.py
│   ├── websocket_sender.py
│   └── mqtt_sender.py
│
config/
└── scenarios/

results/
├── raw/
└── summary/
```

---

## 4. Przepływ działania systemu

1. Wczytanie pliku scenariusza (JSON)
2. Mapowanie do obiektu `ScenarioConfig`
3. Uruchomienie `TestRunner`
4. Generowanie payloadów
5. Wysyłanie wiadomości przez sender
6. Odbiór odpowiedzi z receivera
7. Pomiar czasu RTT
8. Zbieranie metryk
9. Zapis wyników do CSV

---

## 5. TestRunner – centralny komponent

`TestRunner` odpowiada za:

* zarządzanie przebiegiem testu
* tworzenie senderów
* sterowanie pętlą testową
* obsługę wielu klientów (multi-client)
* synchronizację wątków

---

## 6. Tryby wykonania scenariusza

### 6.1 Tryb liczbowy (`count`)

Test wykonywany jest dla określonej liczby wiadomości:

```text
message_count = N
```

---

### 6.2 Tryb czasowy (`duration`)

Test trwa określony czas:

```text
duration_s = T
```

---

## 7. Sterowanie tempem transmisji

System obsługuje dwa sposoby kontroli tempa:

### 7.1 `target_rate_msg_s`

Docelowa liczba wiadomości na sekundę.

### 7.2 `interval_ms`

Stały odstęp między wiadomościami.

### Priorytet:

```text
target_rate_msg_s > interval_ms > brak ograniczeń
```

---

## 8. Obsługa wielu klientów (multi-client)

System umożliwia symulację wielu równoległych klientów.

### Mechanizm:

* dla każdego klienta tworzony jest osobny wątek
* każdy klient posiada:

  * własny sender
  * własne połączenie
* każdy klient wykonuje niezależną pętlę testową

### Parametr:

```json
"concurrent_clients": N
```

---

## 9. Generowanie payloadu

Payload zawiera:

* `scenario_id`
* `run_number`
* `message_id`
* `client_id`
* `client_send_ts`
* `artificial_delay_ms`
* dane losowe

---

## 10. Obsługa opóźnień

System umożliwia symulację opóźnienia odpowiedzi:

```json
"artificial_delay_ms": 500
```

Receiver:

* odczytuje wartość
* wykonuje `sleep()`
* dopiero potem wysyła odpowiedź

---

## 11. Metryki pomiarowe

### 11.1 Latency (RTT)

```text
latency = receive_timestamp - send_timestamp
```

---

### 11.2 Throughput

```text
throughput_msg_s = liczba_success / czas_testu
```

➡️ liczony globalnie (dla wszystkich klientów)

---

### 11.3 Success Rate

```text
success_rate = success / total_messages
```

---

### 11.4 Error Rate

```text
error_rate = errors / total_messages
```

---

### 11.5 Zużycie zasobów

System monitoruje:

* CPU
* RAM
* ruch sieciowy

---

## 12. Obsługa protokołów

### 12.1 HTTP

* model request–response
* każde żądanie niezależne

---

### 12.2 WebSocket

* jedno połączenie
* komunikacja dwukierunkowa

---

### 12.3 MQTT

* publish–subscribe
* broker jako pośrednik
* ACK realizowany przez osobny topic

---

## 13. Format wyników

### 13.1 Wyniki szczegółowe (`raw`)

Każda wiadomość:

* scenario_id
* run_number
* message_id
* client_id
* latency
* status
* error

---

### 13.2 Wyniki zbiorcze (`summary`)

* średnia latencja
* throughput
* success rate
* CPU / RAM

---

## 14. Skalowalność systemu

System umożliwia analizę:

* wpływu liczby klientów
* granicy wydajności systemu
* punktu nasycenia (saturation point)

---

## 15. Podsumowanie

System testowy umożliwia:

* automatyzację eksperymentów
* porównanie protokołów komunikacyjnych
* analizę wydajności i niezawodności
* symulację rzeczywistych warunków IoT

Stanowi on kompletną platformę do przeprowadzenia badań eksperymentalnych w pracy magisterskiej.
