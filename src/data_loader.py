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

        self.raw_data = pd.concat(dfs, axis=1, join="outer")
        self.close_prices = self.raw_data["close"]
        self.open_prices = self.raw_data["open"]

    def get_daily_returns(self, price_type: str = "close") -> pd.DataFrame:
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

    def get_total_returns(self, price_type: str = "close") -> pd.DataFrame:
        price_map = {
            "close": (self.close_prices, "close_returns"),
            "open": (self.open_prices, "open_returns"),
        }

        if price_type not in price_map:
            raise ValueError(f"Unsupported price_type: {price_type}")

        prices, attr_name = price_map[price_type]
        overall_returns = getattr(self, attr_name)

        if overall_returns is None:
            if prices is None:
                raise ValueError(f"{price_type.capitalize()} prices not loaded")

            first_prices = prices.bfill().iloc[0]
            overall_returns = (prices - first_prices) / first_prices * 100

            setattr(self, attr_name, overall_returns)

        return overall_returns

    def comparison_df_prep(self, combinations: list) -> pd.DataFrame:

        df = self.get_total_returns(price_type="close")

        data_combined = []

        for symbol_pair in combinations:
            found_symbols = [s for s in symbol_pair if s in df.columns]

            temp_df = df[found_symbols].copy().dropna()

            temp_df = temp_df.reset_index()
            temp_df.columns.values[0] = 'date'

            temp_df_melted = temp_df.melt(id_vars='date', var_name='symbol', value_name='price_perc_change')
            temp_df_melted['pair'] = f"{symbol_pair[0]} vs {symbol_pair[1]}"

            data_combined.append(temp_df_melted)

        final_df = pd.concat(data_combined)
        return final_df

    def sma_data_prep(self, symbols: list, n: int = 200, n_std : int = 2) -> dict:
        if self.close_prices is None:
            raise ValueError("Data not loaded")

        combined_dict = {}

        for symbol in symbols:
            if symbol not in self.close_prices.columns:
                raise ValueError(f"Symbol {symbol} not found in close_prices")

            prices = self.close_prices[symbol].dropna()
            sma = prices.rolling(window=n).mean()
            std = prices.rolling(window=n).std()
            upper_band = sma + (std * n_std)
            lower_band = sma - (std * n_std)

            symbol_df = pd.DataFrame({
                "price": prices,
                "symbol": symbol,
                "sma" : sma,
                "upper_band": upper_band,
                "lower_band": lower_band
            }).dropna().reset_index()

            combined_dict[symbol] = symbol_df

        return combined_dict





