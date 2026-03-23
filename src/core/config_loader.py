import json
from pathlib import Path
from typing import List

from src.core.scenario import ScenarioConfig


class ConfigLoader:
    @staticmethod
    def load_scenario(path: str) -> ScenarioConfig:
        config_path = Path(path)
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return ScenarioConfig.from_dict(data)

    @staticmethod
    def load_all_scenarios(directory: str) -> List[ScenarioConfig]:
        scenarios = []
        for path in sorted(Path(directory).glob("*.json")):
            scenarios.append(ConfigLoader.load_scenario(str(path)))
        return scenarios