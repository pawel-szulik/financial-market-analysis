import pandas as pd
from pathlib import Path

from .config import NAMES

def data_prep_for_concat(extra_df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes unnecessary columns and adds a multiindex.
    :param extra_df: contains data to be connected to the main dataframe
    :return: modified extra_df
    """

    if extra_df.empty:
        raise ValueError("Empty dataframe")

    symbol = extra_df["symbol"].iloc[0]
    df = extra_df.copy()

    df = df.drop(columns=["change", "changePercent"])
    df = df.set_index("date")

    df.columns = pd.MultiIndex.from_product([df.columns, [symbol]])

    return df


class DataManager:
    """
    Manages the database

    Attributes
    ----------
    path: pathlib.Path
    raw_data: pd.DataFrame | None
    close_prices: pd.DataFrame | None
    open_prices: pd.DataFrame | None
    close_returns: pd.DataFrame | None
    """
    def __init__(self, database_path: str | Path):
        self.path = Path(database_path)

        self.raw_data: pd.DataFrame | None = None
        self.close_prices: pd.DataFrame | None = None
        self.open_prices: pd.DataFrame | None = None

        self.close_returns: pd.DataFrame | None = None

    def load_everything(self, selected_files: list[str] | None = None):
        """
        Loads all CSV files from the given list found in self.path.
        param: selected_files: list[str] | None
        """
        dfs = []
        found_files = {file.name: file for file in self.path.rglob("*.csv")}
        if not found_files:
            raise ValueError(f"No csv files found in {self.path}")

        if selected_files is not None:
            missing = set(selected_files) - set(found_files)
            if missing:
                raise ValueError(f"Files not found: {missing}")
            files_to_load = selected_files
        else:
            files_to_load = found_files.keys()

        for file_name in files_to_load:
            file_path = found_files[file_name]

            try:
                df = pd.read_csv(file_path, parse_dates=["date"])

                prepared = data_prep_for_concat(df)
                dfs.append(prepared)

            except Exception as e:
                raise RuntimeError(f"Error reading file {file_name}: {e}") from e

        if not dfs:
            raise ValueError(f"No data loaded")

        self.raw_data = pd.concat(dfs, axis=1, join="outer").rename(columns=NAMES)
        self.close_prices = self.raw_data["close"]
        self.open_prices = self.raw_data["open"]

        self.close_returns = self.close_prices.pct_change().dropna()



