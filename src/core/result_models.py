from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class MessageResult:
    """
    Model pojedynczej wiadomości testowej (rekord w pliku CSV - dane surowe).

    Pola odpowiadają kolumnom w tabeli wyników:

    scenario_id          - identyfikator scenariusza testowego
    protocol             - użyty protokół komunikacyjny (http/mqtt/websocket)
    run_number           - numer powtórzenia scenariusza
    message_id           - identyfikator wiadomości w danym przebiegu

    send_timestamp       - czas wysłania wiadomości (sekundy, time.time())
    receive_timestamp    - czas otrzymania odpowiedzi (sekundy, time.time())

    latency_ms           - opóźnienie transmisji (RTT) w milisekundach
                           (receive_timestamp - send_timestamp)

    status               - status operacji:
                           "success" - wiadomość poprawnie dostarczona
                           "error"   - błąd transmisji lub timeout

    payload_size         - rozmiar wysłanej wiadomości (w bajtach)
    response_size        - rozmiar odpowiedzi (w bajtach)

    http_status_code     - kod odpowiedzi HTTP (jeśli dotyczy)
    error_message        - opis błędu (jeśli wystąpił)
    """
    scenario_id: str
    protocol: str
    run_number: int
    message_id: int
    client_id: int
    send_timestamp: float
    receive_timestamp: float
    latency_ms: float
    status: str
    payload_size: int
    response_size: int
    http_status_code: Optional[int] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TestRunResult:
    """
    Model podsumowania pojedynczego przebiegu scenariusza (rekord w CSV summary).

    Pola odpowiadają kolumnom w tabeli wyników zagregowanych:

    scenario_id              - identyfikator scenariusza
    protocol                 - użyty protokół
    run_number               - numer powtórzenia testu

    start_time               - czas rozpoczęcia testu (timestamp)
    end_time                 - czas zakończenia testu (timestamp)
    duration_s               - całkowity czas trwania testu (sekundy)

    messages_sent            - liczba wysłanych wiadomości
    messages_received        - liczba poprawnie odebranych wiadomości
    messages_failed          - liczba nieudanych transmisji

    success_rate             - skuteczność transmisji (%)
                               (messages_received / messages_sent * 100)

    avg_latency_ms           - średnie opóźnienie (ms)
    min_latency_ms           - minimalne opóźnienie (ms)
    max_latency_ms           - maksymalne opóźnienie (ms)

    throughput_msg_s         - przepustowość (wiadomości na sekundę)\
    

    --- METRYKI SYSTEMOWE ---

    avg_cpu_percent_process  - średnie użycie CPU procesu (%)
    max_cpu_percent_process  - maksymalne użycie CPU procesu (%)

    avg_memory_rss_mb        - średnie zużycie RAM (MB)
    max_memory_rss_mb        - maksymalne zużycie RAM (MB)

    total_net_bytes_sent     - całkowita liczba wysłanych bajtów (system)
    total_net_bytes_recv     - całkowita liczba odebranych bajtów (system)
    """
    scenario_id: str
    protocol: str
    run_number: int
    start_time: float
    end_time: float
    duration_s: float
    messages_sent: int
    messages_received: int
    messages_failed: int
    success_rate: float
    avg_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    throughput_msg_s: float

    avg_cpu_percent_process: float = 0.0
    max_cpu_percent_process: float = 0.0
    avg_memory_rss_mb: float = 0.0
    max_memory_rss_mb: float = 0.0
    total_net_bytes_sent: int = 0
    total_net_bytes_recv: int = 0

    def to_dict(self) -> dict:
        return asdict(self)