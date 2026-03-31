import time
from typing import List, Tuple

from src.core.metrics_collector import MetricsCollector
from src.core.payload_generator import PayloadGenerator
from src.core.result_models import MessageResult, TestRunResult
from src.core.scenario import ScenarioConfig
from src.core.system_monitor import SystemMonitor
from src.senders.base_sender import BaseSender
from src.senders.http_sender import HTTPSender
from src.senders.mqtt_sender import MQTTSender
from src.senders.websocket_sender import WebSocketSender


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

        if scenario.protocol == "websocket":
            return WebSocketSender(
                host=scenario.host,
                port=scenario.port,
                endpoint=scenario.endpoint_or_topic,
            )

        if scenario.protocol == "mqtt":
            return MQTTSender(
                host=scenario.host,
                port=scenario.port,
                topic=scenario.endpoint_or_topic,
                qos=scenario.qos if scenario.qos is not None else 0,
            )

        raise NotImplementedError(f"Protocol not implemented yet: {scenario.protocol}")

    def run_scenario(self, scenario: ScenarioConfig) -> Tuple[List[MessageResult], List[TestRunResult]]:
        all_raw_results: List[MessageResult] = []
        all_summaries: List[TestRunResult] = []

        for run_number in range(1, scenario.repetitions + 1):
            print(f'[{run_number}/{scenario.repetitions}] - repetitions')
            raw_results, summary = self.run_single_iteration(scenario, run_number)
            all_raw_results.extend(raw_results)
            all_summaries.append(summary)

        return all_raw_results, all_summaries

    def run_single_iteration(
        self,
        scenario: ScenarioConfig,
        run_number: int,
    ) -> Tuple[List[MessageResult], TestRunResult]:
        sender = self.create_sender(scenario)
        metrics = MetricsCollector()
        monitor = SystemMonitor(sample_interval=0.2)

        metrics.reset()
        sender.connect()
        monitor.start()
        start_time = time.time()

        try:
            self._execute_loop(
                sender=sender,
                scenario=scenario,
                run_number=run_number,
                metrics=metrics,
                test_start_time=start_time,
            )
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

    def _execute_loop(
        self,
        sender: BaseSender,
        scenario: ScenarioConfig,
        run_number: int,
        metrics: MetricsCollector,
        test_start_time: float,
    ) -> None:
        message_id = 1
        next_send_time = test_start_time

        while self._should_continue(
            scenario=scenario,
            test_start_time=test_start_time,
            current_message_id=message_id,
        ):
            
            self._wait_until_scheduled_time(
                scenario=scenario,
                next_send_time=next_send_time,
            )

            payload = self.payload_generator.generate(
                payload_type=scenario.payload_type,
                size=scenario.message_size,
                message_id=message_id,
                scenario_id=scenario.scenario_id,
                run_number=run_number,
                artificial_delay_ms=scenario.artificial_delay_ms,
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

            message_id += 1
            next_send_time = self._compute_next_send_time(
                scenario=scenario,
                current_send_time=send_ts,
                previous_next_send_time=next_send_time,
            )

    def _should_continue(
        self,
        scenario: ScenarioConfig,
        test_start_time: float,
        current_message_id: int,
    ) -> bool:
        if scenario.execution_mode == "count":
            print(f'{scenario.scenario_id} | {current_message_id}/{scenario.message_count} - message count')
            return scenario.message_count is not None and current_message_id <= scenario.message_count

        if scenario.execution_mode == "duration":
            elapsed = time.time() - test_start_time
            if int(elapsed*1000) % 1000 == 0: print(f'{scenario.scenario_id} | {int(elapsed)}s - message duration')
            
            return scenario.duration_s is not None and elapsed < scenario.duration_s

        return False

    def _wait_until_scheduled_time(
        self,
        scenario: ScenarioConfig,
        next_send_time: float,
    ) -> None:
        if scenario.target_rate_msg_s is None and scenario.interval_ms <= 0:
            return

        now = time.time()
        sleep_time = next_send_time - now
        if sleep_time > 0:
            time.sleep(sleep_time)

    def _compute_next_send_time(
        self,
        scenario: ScenarioConfig,
        current_send_time: float,
        previous_next_send_time: float,
    ) -> float:
        if scenario.target_rate_msg_s is not None:
            interval = 1.0 / scenario.target_rate_msg_s
            return max(previous_next_send_time + interval, current_send_time)

        if scenario.interval_ms > 0:
            return current_send_time + (scenario.interval_ms / 1000.0)

        return current_send_time