import pandas as pd


class DataLoader:
    @staticmethod
    def load_raw(path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    @staticmethod
    def load_summary(path: str) -> pd.DataFrame:
        return pd.read_csv(path)