from abc import ABC, abstractmethod


class BaseSender(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def send_and_wait(self, payload: str, timeout_ms: int) -> dict:
        pass