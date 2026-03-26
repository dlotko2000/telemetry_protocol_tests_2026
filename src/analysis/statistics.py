import pandas as pd


class Statistics:
    @staticmethod
    def latency_stats(df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("protocol")["latency_ms"].agg([
            "mean",
            "median",
            "min",
            "max",
            "std"
        ]).reset_index()

    @staticmethod
    def success_rate(df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("protocol")["success_rate"].mean().reset_index()

    @staticmethod
    def throughput(df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("protocol")["throughput_msg_s"].mean().reset_index()

    @staticmethod
    def resource_usage(df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("protocol")[[
            "avg_cpu_percent_process",
            "avg_memory_rss_mb"
        ]].mean().reset_index()