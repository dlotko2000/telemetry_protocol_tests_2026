import time
from typing import List, Tuple

from src.core.system_monitor import SystemMonitor
from src.core.metrics_collector import MetricsCollector
from src.core.payload_generator import PayloadGenerator
from src.core.result_models import MessageResult, TestRunResult
from src.core.scenario import ScenarioConfig
from src.senders.base_sender import BaseSender
from src.senders.http_sender import HTTPSender


class TestRunner:
    def __init__(self) -> None:
        self.payload_generator = PayloadGenerator()

    def create_sender(self, scenario: ScenarioConfig) -> BaseSender:
        if scenario.protocol == "http":
            return HTTPSender(
                host=scenario.host,
                port=scenario.port,
                endpoint=scenario.endpoint_or_topic,
            )

        raise NotImplementedError(f"Protocol not implemented yet: {scenario.protocol}")

    def run_scenario(self, scenario: ScenarioConfig) -> Tuple[List[MessageResult], List[TestRunResult]]:
        all_raw_results: List[MessageResult] = []
        all_summaries: List[TestRunResult] = []

        for run_number in range(1, scenario.repetitions + 1):
            raw_results, summary = self.run_single_iteration(scenario, run_number)
            all_raw_results.extend(raw_results)
            all_summaries.append(summary)

        return all_raw_results, all_summaries

    def run_single_iteration(
        self,
        scenario: ScenarioConfig,
        run_number: int
    ) -> Tuple[List[MessageResult], TestRunResult]:
        monitor = SystemMonitor(sample_interval=0.2)
        sender = self.create_sender(scenario)
        metrics = MetricsCollector()
        metrics.reset()

        sender.connect()
        monitor.start()
        start_time = time.time()

        try:
            for message_id in range(1, scenario.message_count + 1):
                payload = self.payload_generator.generate(
                    payload_type=scenario.payload_type,
                    size=scenario.message_size,
                    message_id=message_id,
                    scenario_id=scenario.scenario_id,
                    run_number=run_number,
                )

                send_ts = time.time()

                try:
                    response_data = sender.send_and_wait(payload, scenario.timeout_ms)
                    receive_ts = time.time()
                    latency_ms = (receive_ts - send_ts) * 1000.0

                    result = MessageResult(
                        scenario_id=scenario.scenario_id,
                        protocol=scenario.protocol,
                        run_number=run_number,
                        message_id=message_id,
                        send_timestamp=send_ts,
                        receive_timestamp=receive_ts,
                        latency_ms=latency_ms,
                        status=response_data["status"],
                        payload_size=len(payload.encode("utf-8")),
                        response_size=response_data.get("response_size", 0),
                        http_status_code=response_data.get("http_status_code"),
                        error_message=None,
                    )
                except Exception as e:
                    receive_ts = time.time()
                    latency_ms = (receive_ts - send_ts) * 1000.0

                    result = MessageResult(
                        scenario_id=scenario.scenario_id,
                        protocol=scenario.protocol,
                        run_number=run_number,
                        message_id=message_id,
                        send_timestamp=send_ts,
                        receive_timestamp=receive_ts,
                        latency_ms=latency_ms,
                        status="error",
                        payload_size=len(payload.encode("utf-8")),
                        response_size=0,
                        http_status_code=None,
                        error_message=str(e),
                    )

                metrics.record_message_result(result)
                time.sleep(scenario.interval_ms / 1000.0)

        finally:
            end_time = time.time()
            monitor.stop()
            sender.disconnect()

        resource_summary = monitor.get_summary()

        summary = metrics.build_summary(
            scenario_id=scenario.scenario_id,
            protocol=scenario.protocol,
            run_number=run_number,
            start_time=start_time,
            end_time=end_time,
            resource_summary=resource_summary,
        )

        return metrics.get_raw_results(), summary