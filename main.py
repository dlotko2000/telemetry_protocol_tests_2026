import argparse
from datetime import datetime

from src.core.config_loader import ConfigLoader
from src.core.test_runner import TestRunner
from src.storage.csv_writer import CSVWriter


def run_single_scenario(path: str) -> None:
    scenario = ConfigLoader.load_scenario(path)
    runner = TestRunner()

    raw_results, summaries = runner.run_scenario(scenario)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"results/raw/{scenario.scenario_id}_{timestamp}_raw.csv"
    summary_path = f"results/summary/{scenario.scenario_id}_{timestamp}_summary.csv"

    CSVWriter.write(raw_path, [r.to_dict() for r in raw_results])
    CSVWriter.write(summary_path, [s.to_dict() for s in summaries])

    print(f"Scenario finished: {scenario.name}")
    print(f"Raw results saved to: {raw_path}")
    print(f"Summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="Telemetry Protocol Test Runner")
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--scenario", required=True, help="Path to scenario JSON file")
    args = parser.parse_args()

    if args.command == "run":
        run_single_scenario(args.scenario)


if __name__ == "__main__":
    main()