import os

from src.analysis.data_loader import DataLoader
from src.analysis.statistics import Statistics
from src.analysis.charts import ChartGenerator


class Analyzer:

    def __init__(self, raw_path: str, summary_path: str):
        self.raw_df = DataLoader.load_raw(raw_path)
        self.summary_df = DataLoader.load_summary(summary_path)

        os.makedirs("results/charts", exist_ok=True)

    def run(self):
        self._latency_analysis()
        self._throughput_analysis()
        self._success_analysis()
        self._resource_analysis()
        self._boxplot()

    def _latency_analysis(self):
        stats = Statistics.latency_stats(self.raw_df)
        print("\nLatency stats:\n", stats)

        ChartGenerator.bar_chart(
            stats,
            x="protocol",
            y="mean",
            title="Average latency comparison",
            ylabel="Latency (ms)",
            output_path="results/charts/latency.png"
        )

    def _throughput_analysis(self):
        stats = Statistics.throughput(self.summary_df)
        print("\nThroughput:\n", stats)

        ChartGenerator.bar_chart(
            stats,
            x="protocol",
            y="throughput_msg_s",
            title="Throughput comparison",
            ylabel="Messages per second",
            output_path="results/charts/throughput.png"
        )

    def _success_analysis(self):
        stats = Statistics.success_rate(self.summary_df)
        print("\nSuccess rate:\n", stats)

        ChartGenerator.bar_chart(
            stats,
            x="protocol",
            y="success_rate",
            title="Success rate comparison",
            ylabel="%",
            output_path="results/charts/success_rate.png"
        )

    def _resource_analysis(self):
        stats = Statistics.resource_usage(self.summary_df)
        print("\nResource usage:\n", stats)

        ChartGenerator.bar_chart(
            stats,
            x="protocol",
            y="avg_cpu_percent_process",
            title="CPU usage comparison",
            ylabel="CPU %",
            output_path="results/charts/cpu.png"
        )

        ChartGenerator.bar_chart(
            stats,
            x="protocol",
            y="avg_memory_rss_mb",
            title="Memory usage comparison",
            ylabel="RAM (MB)",
            output_path="results/charts/memory.png"
        )

    def _boxplot(self):
        ChartGenerator.boxplot_latency(
            self.raw_df,
            output_path="results/charts/latency_boxplot.png"
        )