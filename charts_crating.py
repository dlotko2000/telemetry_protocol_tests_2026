from src.analysis.analyze import Analyzer

Analyzer(
    raw_path="results/raw/S3_MQTT_20260326_213559_raw.csv",
    summary_path="results/summary/S3_MQTT_20260326_213559_summary.csv"
).run()