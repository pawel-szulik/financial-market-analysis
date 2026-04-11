import pandas as pd
from pathlib import Path


def data_prep_for_concat(extra_df: pd.DataFrame) -> pd.DataFrame:
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

def data_concat(folder_name: str, selected_files_list: list) -> pd.DataFrame:
    """
    This function scans selected folder for csv files, then it inner joins them into a one big dataframe.
    :param folder_name: the name of a folder which is being scanned for csv files
    :param selected_files_list: names of csv files which we want to combine into a dataframe.
    :return:
    """
    dfs = []
    base_path = Path(folder_name)
    found_files = {file.name: file for file in base_path.rglob("*.csv")}

    for file_name in selected_files_list:
        if file_name in found_files:
            file_path = found_files[file_name]
            try:
                df = pd.read_csv(file_path, parse_dates=["date"])

                prepared = data_prep_for_concat(df)
                dfs.append(prepared)

            except Exception as e:
                print(f"An Error occurred, while reading a file {file_name}: {e}")

    if not dfs:
        print(f"No csv files found in {folder_name}")

    final_df = pd.concat(dfs, axis=1, join="inner")
    return final_df

if __name__ == "__main__":
    selected_files = ["BZUSD.csv", "GCUSD.csv", "SIUSD.csv", "BTCUSD.csv", "ETHUSD.csv", "EURUSD.csv", "GBPUSD.csv", "USDCAD.csv",
                      "USDCHF.csv", "USDCNH.csv", "USDJPY.csv", "USDPLN.csv", "USDRUB.csv", "DJI.csv", "FTSE.csv", "GSPC.csv", "HSI.csv",
                      "IXIC.csv", "N225.csv", "RUT.csv", "STOXX50E.csv", "VIX.csv"]

    main_df = data_concat("database_2026-03-04", selected_files)
    main_df.to_csv("prepared_data.csv")