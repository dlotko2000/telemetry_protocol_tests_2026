import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def bar_chart(df, x, y, title, ylabel, output_path):
        plt.figure()
        plt.bar(df[x], df[y])
        plt.title(title)
        plt.xlabel("Protocol")
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    @staticmethod
    def boxplot_latency(df, output_path):
        plt.figure()
        df.boxplot(column="latency_ms", by="protocol")
        plt.title("Latency distribution")
        plt.suptitle("")
        plt.xlabel("Protocol")
        plt.ylabel("Latency (ms)")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()