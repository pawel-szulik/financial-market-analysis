import pandas as pd
from pathlib import Path

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

    df.columns = pd.MultiIndex.from_product([[symbol], df.columns])

    return df


class DataManager:
    """
    Manages the database

    Attributes
    ----------
    path: pathlib.Path
    raw_data: pd.DataFrame | None
    close_prices: pd.DataFrame | None
    close_returns: pd.DataFrame | None
    open_prices: pd.DataFrame | None
    open_returns: pd.DataFrame | None
    """
    def __init__(self, database_path: str | Path):
        self.path = Path(database_path)
        self.raw_data: pd.DataFrame | None = None
        self.close_prices: pd.DataFrame | None = None
        self.close_returns: pd.DataFrame | None = None
        self.open_prices: pd.DataFrame | None = None
        self.open_returns: pd.DataFrame | None = None

    def load_everything(self, selected_files: list[str]):
        """
        Loads all CSV files from the given list found in self.path.
        param: selected_files: list[str]
        """
        dfs = []
        found_files = {file.name: file for file in self.path.rglob("*.csv")}

        for file_name in selected_files:
            if file_name in found_files:
                file_path = found_files[file_name]
                try:
                    df = pd.read_csv(file_path, parse_dates=["date"])

                    prepared = data_prep_for_concat(df)
                    dfs.append(prepared)

                except Exception as e:
                    raise RuntimeError(f"Error reading file {file_name}") from e

        if not dfs:
            raise ValueError(f"No csv files found in {self.path}")

        self.raw_data = pd.concat(dfs, axis=1, join="outer")
        self.close_prices = self.raw_data["close"]
        self.open_prices = self.raw_data["open"]

    def get_returns(self, price_type: str = "close") -> pd.DataFrame:
        """
        Calculates percentage returns for given price type.
        param: price_type: str
        return: pd.DataFrame
        """
        price_map = {
            "close": (self.close_prices, "close_returns"),
            "open": (self.open_prices, "open_returns"),
        }

        if price_type not in price_map:
            raise ValueError(f"Unsupported price_type: {price_type}")

        prices, attr_name = price_map[price_type]
        returns = getattr(self, attr_name)

        if returns is None:
            if prices is None:
                raise ValueError(f"{price_type.capitalize()} prices not loaded")

            returns = prices.pct_change().dropna()
            setattr(self, attr_name, returns)

        return returns

