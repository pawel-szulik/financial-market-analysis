import pandas as pd
from pathlib import Path

def prepare_price_df(extra_df: pd.DataFrame) -> pd.DataFrame:
    """
    Counts the price change, converts "date" to datetime, removes unnecessary columns and adds a multiindex
    :param extra_df: contains data to be connected to the main dataframe
    :return: modified extra_df
    """
    symbol = extra_df["symbol"].iloc[0]
    df = extra_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["perc_change"] = (df["close"] / df["close"].shift(1) - 1) * 100

    df = df[["date", "close", "perc_change"]].set_index("date")

    df.columns = pd.MultiIndex.from_product([[symbol], df.columns])

    return df

def load_entire_dataset(database_path: str) -> pd.DataFrame:
    """
    Loads all .csv files from the specified folder and converts them into a final DataFrame for further analysis.
    :param database_path:
    :return: final DataFrame
    """
    dfs = []

    for file in Path(database_path).rglob("*.csv"):
        try:
            df = pd.read_csv(str(file), parse_dates=["date"])

            prepared = prepare_price_df(df)
            dfs.append(prepared)

        except Exception as e:
            print(f"Error reading file {file}: {e}")

    final_df = pd.concat(dfs, axis=1, join="inner")
    return final_df

if __name__ == "__main__":
    main_df = load_entire_dataset("price_charts_database_2026-03-04")
    main_df.to_csv("prepared_data.csv")