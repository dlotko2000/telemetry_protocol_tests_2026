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
    message_count: int
    message_size: int
    interval_ms: int
    timeout_ms: int
    repetitions: int
    qos: Optional[int] = None
    concurrent_clients: int = 1
    payload_type: str = "text"

    @classmethod
    def from_dict(cls, data: dict) -> "ScenarioConfig":
        scenario = cls(
            scenario_id=data["scenario_id"],
            name=data["name"],
            protocol=data["protocol"].lower(),
            host=data["host"],
            port=int(data["port"]),
            endpoint_or_topic=data["endpoint_or_topic"],
            message_count=int(data["message_count"]),
            message_size=int(data["message_size"]),
            interval_ms=int(data["interval_ms"]),
            timeout_ms=int(data["timeout_ms"]),
            repetitions=int(data["repetitions"]),
            qos=data.get("qos"),
            concurrent_clients=int(data.get("concurrent_clients", 1)),
            payload_type=data.get("payload_type", "text"),
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

    def to_dict(self) -> dict:
        return asdict(self)