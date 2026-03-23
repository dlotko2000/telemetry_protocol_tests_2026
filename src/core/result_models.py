from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class MessageResult:
    scenario_id: str
    protocol: str
    run_number: int
    message_id: int
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