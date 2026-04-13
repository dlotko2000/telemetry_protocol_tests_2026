# Dokumentacja konfiguracji scenariuszy testowych

## 1. Wprowadzenie

Konfiguracja scenariuszy testowych w systemie została zrealizowana przy użyciu plików w formacie JSON.
Każdy scenariusz definiuje parametry komunikacji, sposób generowania obciążenia oraz warunki przeprowadzania eksperymentu.

Dzięki zastosowaniu zunifikowanego formatu możliwe jest przeprowadzanie porównywalnych testów dla różnych protokołów komunikacyjnych (HTTP, WebSocket, MQTT).

---

## 2. Struktura ogólna pliku

Każdy scenariusz opisany jest jako pojedynczy obiekt JSON:

```json
{
  "scenario_id": "...",
  "name": "...",
  "protocol": "...",
  "host": "...",
  "port": ...,
  "endpoint_or_topic": "...",

  "execution_mode": "...",
  "message_count": ...,
  "duration_s": ...,

  "message_size": ...,
  "interval_ms": ...,
  "target_rate_msg_s": ...,

  "timeout_ms": ...,
  "repetitions": ...,

  "payload_type": "...",
  "artificial_delay_ms": ...,

  "qos": ...,
  "concurrent_clients": ...
}
```

---

## 3. Opis pól konfiguracji

### 3.1. Identyfikacja scenariusza

#### `scenario_id`

Unikalny identyfikator scenariusza.

* Typ: `string`
* Przykład: `"S1_HTTP"`
* Wykorzystanie: identyfikacja w wynikach (CSV, wykresy)

---

#### `name`

Opisowa nazwa scenariusza.

* Typ: `string`
* Przykład: `"Scenariusz nr 1 - test bazowy"`
* Wykorzystanie: raporty, logi

---

### 3.2. Parametry komunikacji

#### `protocol`

Określa używany protokół komunikacyjny.

* Typ: `string`
* Dozwolone wartości:

  * `"http"`
  * `"websocket"`
  * `"mqtt"`

---

#### `host`

Adres hosta odbiornika.

* Typ: `string`
* Przykład: `"127.0.0.1"`

---

#### `port`

Port usługi komunikacyjnej.

* Typ: `integer`
* Przykłady:

  * HTTP: `8000`
  * WebSocket: `8765`
  * MQTT: `1883`

---

#### `endpoint_or_topic`

Cel komunikacji zależny od protokołu:

* HTTP → endpoint (np. `/telemetry`)

* WebSocket → ścieżka (np. `/ws`)

* MQTT → topic (np. `telemetry/data`)

* Typ: `string`

---

### 3.3. Tryb wykonania testu

#### `execution_mode`

Określa sposób zakończenia testu.

* Typ: `string`
* Wartości:

  * `"count"` → test kończy się po określonej liczbie wiadomości
  * `"duration"` → test trwa określony czas

---

#### `message_count`

Liczba wiadomości do wysłania.

* Typ: `integer | null`
* Wymagane dla: `execution_mode = "count"`

---

#### `duration_s`

Czas trwania testu w sekundach.

* Typ: `integer | null`
* Wymagane dla: `execution_mode = "duration"`

---

### 3.4. Parametry wiadomości

#### `message_size`

Rozmiar wiadomości (payloadu) w bajtach.

* Typ: `integer`
* Przykłady:

  * `32`
  * `256`
  * `1024`
  * `4096`

---

#### `payload_type`

Typ generowanego payloadu.

* Typ: `string`
* Wartości:

  * `"json"`
  * `"text"`

---

### 3.5. Sterowanie tempem wysyłki

#### `interval_ms`

Stały odstęp czasu między wiadomościami.

* Typ: `integer`
* Jednostka: milisekundy
* Przykład: `100` → 10 wiadomości/s

---

#### `target_rate_msg_s`

Docelowa liczba wiadomości na sekundę.

* Typ: `float | null`
* Przykład: `10` → 10 wiadomości/s

---

### 🔹 Priorytet sterowania tempem

System stosuje następującą hierarchię:

```text
target_rate_msg_s > interval_ms > brak ograniczeń
```

* jeśli ustawiono `target_rate_msg_s` → steruje tempem
* jeśli nie → używany `interval_ms`
* jeśli oba brak → maksymalna przepustowość

---

### 3.6. Parametry transmisji

#### `timeout_ms`

Maksymalny czas oczekiwania na odpowiedź.

* Typ: `integer`
* Jednostka: milisekundy
* Przykład: `3000`

---

#### `repetitions`

Liczba powtórzeń scenariusza.

* Typ: `integer`
* Przykład: `5`

---

### 3.7. MQTT (opcjonalne)

#### `qos`

Poziom Quality of Service dla MQTT.

* Typ: `integer | null`
* Wartości:

  * `0` — at most once
  * `1` — at least once
  * `2` — exactly once

---

### 3.8. Symulacja opóźnienia

#### `artificial_delay_ms`

Sztuczne opóźnienie odpowiedzi po stronie odbiornika.

* Typ: `integer`
* Jednostka: milisekundy
* Przykład: `250`

Wartość ta jest przekazywana w payloadzie i wykorzystywana przez receiver.

---

### 3.9. Równoległość

#### `concurrent_clients`

Liczba równoległych klientów.

* Typ: `integer`
* Aktualnie: obsługiwany tryb sekwencyjny (`1`)

---

## 4. Przykładowy scenariusz

```json
{
  "scenario_id": "S3_HTTP",
  "name": "Test wysokiej intensywności",
  "protocol": "http",
  "host": "127.0.0.1",
  "port": 8000,
  "endpoint_or_topic": "/telemetry",

  "execution_mode": "duration",
  "duration_s": 60,

  "message_size": 64,
  "target_rate_msg_s": null,
  "interval_ms": 0,

  "timeout_ms": 1500,
  "repetitions": 3,

  "payload_type": "json",
  "artificial_delay_ms": 0,

  "qos": null,
  "concurrent_clients": 1
}
```

---

## 5. Uwagi implementacyjne

1. Wszystkie scenariusze są przetwarzane przez `ScenarioConfig`.
2. Parametry są walidowane przed uruchomieniem testu.
3. System wspiera dwa tryby:

   * liczbowy (`count`)
   * czasowy (`duration`)
4. W scenariuszach MQTT wymagany jest broker (np. Mosquitto).
5. Opóźnienie (`artificial_delay_ms`) jest realizowane po stronie odbiornika.

---

## 6. Podsumowanie

Zastosowany model konfiguracji umożliwia:

* pełną kontrolę nad przebiegiem testu
* porównywalność wyników między protokołami
* łatwe rozszerzanie scenariuszy
* automatyzację eksperymentów

Stanowi on fundament do przeprowadzenia badań eksperymentalnych nad wydajnością i niezawodnością protokołów komunikacyjnych w systemach IoT.
