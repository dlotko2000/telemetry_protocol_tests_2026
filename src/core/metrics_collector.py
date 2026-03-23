from typing import List

from src.core.result_models import MessageResult, TestRunResult


class MetricsCollector:
    def __init__(self) -> None:
        self.results: List[MessageResult] = []

    def reset(self) -> None:
        self.results = []

    def record_message_result(self, result: MessageResult) -> None:
        self.results.append(result)

    def get_raw_results(self) -> List[MessageResult]:
        return self.results

    def build_summary(
        self,
        scenario_id: str,
        protocol: str,
        run_number: int,
        start_time: float,
        end_time: float,
        resource_summary=None,
    ) -> TestRunResult:
        duration_s = max(end_time - start_time, 1e-9)
        successful = [r for r in self.results if r.status == "success"]
        failed = [r for r in self.results if r.status != "success"]

        latencies = [r.latency_ms for r in successful]

        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        min_latency = min(latencies) if latencies else 0.0
        max_latency = max(latencies) if latencies else 0.0

        messages_sent = len(self.results)
        messages_received = len(successful)
        messages_failed = len(failed)
        success_rate = (messages_received / messages_sent * 100.0) if messages_sent else 0.0
        throughput_msg_s = messages_received / duration_s

        return TestRunResult(
            scenario_id=scenario_id,
            protocol=protocol,
            run_number=run_number,
            start_time=start_time,
            end_time=end_time,
            duration_s=duration_s,
            messages_sent=messages_sent,
            messages_received=messages_received,
            messages_failed=messages_failed,
            success_rate=success_rate,
            avg_latency_ms=avg_latency,
            min_latency_ms=min_latency,
            max_latency_ms=max_latency,
            throughput_msg_s=throughput_msg_s,

            avg_cpu_percent_process=resource_summary.avg_cpu_percent_process if resource_summary else 0.0,
            max_cpu_percent_process=resource_summary.max_cpu_percent_process if resource_summary else 0.0,
            avg_memory_rss_mb=resource_summary.avg_memory_rss_mb if resource_summary else 0.0,
            max_memory_rss_mb=resource_summary.max_memory_rss_mb if resource_summary else 0.0,
            total_net_bytes_sent=resource_summary.total_net_bytes_sent if resource_summary else 0,
            total_net_bytes_recv=resource_summary.total_net_bytes_recv if resource_summary else 0,
        )