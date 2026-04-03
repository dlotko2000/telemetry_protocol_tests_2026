import json
import random
import string
import time


class PayloadGenerator:
    @staticmethod
    def generate(
        payload_type: str,
        size: int,
        message_id: int,
        scenario_id: str,
        run_number: int,
        client_id: int,
        artificial_delay_ms: int = 0,
    ) -> str:
        payload_type = payload_type.lower()

        if payload_type == "json":
            return PayloadGenerator._generate_json(
                size=size,
                message_id=message_id,
                scenario_id=scenario_id,
                run_number=run_number,
                client_id=client_id,
                artificial_delay_ms=artificial_delay_ms,
            )

        return PayloadGenerator._generate_text(
            size=size,
            message_id=message_id,
            scenario_id=scenario_id,
            run_number=run_number,
            artificial_delay_ms=artificial_delay_ms,
        )

    @staticmethod
    def _generate_text(
        size: int,
        message_id: int,
        scenario_id: str,
        run_number: int,
        artificial_delay_ms: int,
    ) -> str:
        header = (
            f"{scenario_id}|run={run_number}|msg={message_id}|"
            f"delay_ms={artificial_delay_ms}|ts={time.time()}|"
        )
        body_size = max(0, size - len(header))
        body = "".join(random.choices(string.ascii_letters + string.digits, k=body_size))
        return header + body

    @staticmethod
    def _generate_json(
        size: int,
        message_id: int,
        scenario_id: str,
        run_number: int,
        artificial_delay_ms: int,
        client_id: int,
    ) -> str:
        base = {
            "scenario_id": scenario_id,
            "run_number": run_number,
            "message_id": message_id,
            "client_send_ts": time.time(),
            "client_id": client_id,
            "artificial_delay_ms": artificial_delay_ms,
            "payload": "",
        }

        raw = json.dumps(base, ensure_ascii=False)
        body_size = max(0, size - len(raw))
        base["payload"] = "".join(random.choices(string.ascii_letters + string.digits, k=body_size))

        return json.dumps(base, ensure_ascii=False)