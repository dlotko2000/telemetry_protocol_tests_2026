import threading
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

import psutil


@dataclass
class ResourceSample:
    timestamp: float
    cpu_percent_process: float
    memory_rss_mb: float
    net_bytes_sent: int
    net_bytes_recv: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResourceSummary:
    avg_cpu_percent_process: float
    max_cpu_percent_process: float
    avg_memory_rss_mb: float
    max_memory_rss_mb: float
    total_net_bytes_sent: int
    total_net_bytes_recv: int

    def to_dict(self) -> dict:
        return asdict(self)


class SystemMonitor:
    def __init__(self, sample_interval: float = 0.2) -> None:
        self.sample_interval = sample_interval
        self.samples: List[ResourceSample] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._process = psutil.Process()

    def start(self) -> None:
        self.samples = []
        self._running = True

        # inicjalizacja pomiarów
        self._process.cpu_percent(interval=None)
        psutil.net_io_counters()

        self._thread = threading.Thread(target=self._sampling_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()

    def _sampling_loop(self) -> None:
        while self._running:
            mem = self._process.memory_info()
            net = psutil.net_io_counters()

            sample = ResourceSample(
                timestamp=time.time(),
                cpu_percent_process=self._process.cpu_percent(interval=None),
                memory_rss_mb=mem.rss / (1024 * 1024),
                net_bytes_sent=net.bytes_sent,
                net_bytes_recv=net.bytes_recv,
            )

            self.samples.append(sample)
            time.sleep(self.sample_interval)

    def get_summary(self) -> ResourceSummary:
        if not self.samples:
            return ResourceSummary(0, 0, 0, 0, 0, 0)

        cpu_vals = [s.cpu_percent_process for s in self.samples]
        mem_vals = [s.memory_rss_mb for s in self.samples]

        first = self.samples[0]
        last = self.samples[-1]

        return ResourceSummary(
            avg_cpu_percent_process=sum(cpu_vals) / len(cpu_vals),
            max_cpu_percent_process=max(cpu_vals),
            avg_memory_rss_mb=sum(mem_vals) / len(mem_vals),
            max_memory_rss_mb=max(mem_vals),
            total_net_bytes_sent=max(0, last.net_bytes_sent - first.net_bytes_sent),
            total_net_bytes_recv=max(0, last.net_bytes_recv - first.net_bytes_recv),
        )