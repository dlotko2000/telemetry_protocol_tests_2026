from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ScenarioConfig:
    scenario_id: str
    name: str
    protocol: str

    host: str
    port: int
    endpoint_or_topic: str

    execution_mode: str = "count"
    message_count: Optional[int] = 1
    duration_s: Optional[int] = None

    message_size: int = 64
    interval_ms: int = 0
    target_rate_msg_s: Optional[float] = None
    timeout_ms: int = 3000
    repetitions: int = 1

    qos: Optional[int] = None
    concurrent_clients: int = 1
    payload_type: str = "json"
    artificial_delay_ms: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> "ScenarioConfig":
        scenario = cls(
            scenario_id=data["scenario_id"],
            name=data["name"],
            protocol=data["protocol"].lower(),
            host=data["host"],
            port=int(data["port"]),
            endpoint_or_topic=data["endpoint_or_topic"],
            execution_mode=data.get("execution_mode", "count").lower(),
            message_count=(
                int(data["message_count"])
                if data.get("message_count") is not None
                else None
            ),
            duration_s=(
                int(data["duration_s"])
                if data.get("duration_s") is not None
                else None
            ),
            message_size=int(data["message_size"]),
            interval_ms=int(data.get("interval_ms", 0)),
            target_rate_msg_s=(
                float(data["target_rate_msg_s"])
                if data.get("target_rate_msg_s") is not None
                else None
            ),
            timeout_ms=int(data["timeout_ms"]),
            repetitions=int(data["repetitions"]),
            qos=data.get("qos"),
            concurrent_clients=int(data.get("concurrent_clients", 1)),
            payload_type=data.get("payload_type", "json"),
            artificial_delay_ms=int(data.get("artificial_delay_ms", 0)),
        )
        scenario.validate()
        return scenario

    def validate(self) -> None:
        if self.protocol not in {"http", "mqtt", "websocket"}:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

        numeric_fields = {
            "port": self.port,
            "message_count": self.message_count,
            "message_size": self.message_size,
            "interval_ms": self.interval_ms,
            "timeout_ms": self.timeout_ms,
            "repetitions": self.repetitions,
            "concurrent_clients": self.concurrent_clients,
        }

        for field_name, value in numeric_fields.items():
            if value < 1:
                raise ValueError(f"{field_name} must be >= 1")

        if not self.host.strip():
            raise ValueError("host cannot be empty")

        if not self.endpoint_or_topic.strip():
            raise ValueError("endpoint_or_topic cannot be empty")
        
        if self.execution_mode not in {"count", "duration"}:
            raise ValueError("execution_mode must be 'count' or 'duration'")

        if self.execution_mode == "count":
            if self.message_count is None or self.message_count < 1:
                raise ValueError("message_count must be >= 1 for execution_mode='count'")

        if self.execution_mode == "duration":
            if self.duration_s is None or self.duration_s < 1:
                raise ValueError("duration_s must be >= 1 for execution_mode='duration'")

        if self.target_rate_msg_s is not None and self.target_rate_msg_s <= 0:
            raise ValueError("target_rate_msg_s must be > 0")

        if self.artificial_delay_ms < 0:
            raise ValueError("artificial_delay_ms must be >= 0")

    def to_dict(self) -> dict:
        return asdict(self)