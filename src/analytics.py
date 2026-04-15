import pandas as pd
import scipy.stats as stats
import numpy as np
from itertools import combinations


def mean_significance(df: pd.DataFrame) -> pd.DataFrame:
    mean = df.mean()
    _, p_v = stats.ttest_1samp(df, popmean=0, axis=0)

    return  pd.DataFrame({
        "mean": mean,
        "p_value": p_v})


def sign_test(df: pd.DataFrame, alternative: str) -> pd.DataFrame:
    results = {}

    for col in df.columns:
        series = df[col].dropna()

        n = len(series)
        k = (series > 0).sum()

        test = stats.binomtest(k, n, p=0.5, alternative=alternative)

        results[col] = {
            "win_rate": (k / n) * 100,
            "p_value": test.pvalue,
        }

    return pd.DataFrame(results).T

def correlations(df: pd.DataFrame, corr_type: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes a table of selected correlation coefficients along with their p-values.
    :param df: pd.DataFrame
    :param corr_type: str
    :return: tuple[pd.DataFrame, pd.DataFrame]
    """
    cols = df.columns
    corrs = pd.DataFrame(index=cols, columns=cols)
    p_vals = pd.DataFrame(index=cols, columns=cols)

    for idx_i, i in enumerate(cols):
        for idx_j, j in enumerate(cols):
            if idx_j == idx_i:
                corrs.loc[i, j] = 1
                p_vals.loc[i, j] = 0
            if idx_j <= idx_i:
                continue
            valid = df[[i, j]].dropna()
            if corr_type == "pearson":
                c, p = stats.pearsonr(valid[i], valid[j])
            elif corr_type == "spearman":
                c, p = stats.spearmanr(valid[i], valid[j])
            else:
                raise ValueError("corr_type must be 'pearson' or 'spearman'")

            corrs.loc[i, j] = c
            corrs.loc[j, i] = c

            p_vals.loc[i, j] = p
            p_vals.loc[j, i] = p

    return corrs.astype(float), p_vals.astype(float)

def corr_score(corrs: pd.DataFrame, pvals: pd.DataFrame) -> pd.Series:
    """
    Sums absolute significant correlations and returns a score for each asset.
    :param corrs: pd.DataFrame
    :param pvals: pd.DataFrame
    :return: pd.Series
    """
    mask = pvals < 0.05
    filtered_corrs = corrs.abs() * mask

    arr = filtered_corrs.to_numpy(copy=True)
    np.fill_diagonal(arr, 0)

    score = arr.sum(axis=1)
    return pd.Series(score, index=filtered_corrs.index).sort_values(ascending=False)


def regression(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes a table of linear regression slope coefficients and p-value significance tests.
    :param df: pd.DataFrame
    :return: tuple[pd.DataFrame, pd.DataFrame]
    """

    cols = df.columns
    slopes = pd.DataFrame(index=cols, columns=cols)
    p_vals = pd.DataFrame(index=cols, columns=cols)

    for i in cols:
        for j in cols:
            if i == j:
                slopes.loc[i, j] = 1
                p_vals.loc[i, j] = 0
                continue
            valid = df[[i, j]].dropna()
            x = valid[i].values
            y = valid[j].values

            reg = stats.linregress(x, y)

            slopes.loc[i, j] = reg.slope
            p_vals.loc[i, j] = reg.pvalue

    return slopes.astype(float), p_vals.astype(float)


def longest_drawdown(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for col in df.columns:
        prices = df[col].dropna()

        run_max = prices.cummax()
        under = prices < run_max

        group_id = (under != under.shift()).cumsum()

        periods = []

        for _, group in under.groupby(group_id):
            if group.iloc[0]:  # tylko okresy under water
                start = group.index[0]
                end = group.index[-1]
                length = (end - start).days

                periods.append({
                    "start": start,
                    "end": end,
                    "length": length
                })

        if periods:
            longest = max(periods, key=lambda x: x["length"])
        else:
            longest = {"start": None, "end": None, "length": 0}

        results.append({
            "asset": col,
            "start": longest["start"],
            "end": longest["end"],
            "length": longest["length"]
        })

    return pd.DataFrame(results)


def make_pairs(symbols: list[str]) -> list[tuple[str, str]]:
    return list(combinations(symbols, 2))


def comparison_df_prep(df: pd.DataFrame, combinations_l: list) -> pd.DataFrame:

    data_combined = []

    for symbol_pair in combinations_l:
        found_symbols = [s for s in symbol_pair if s in df.columns]

        temp_df = df[found_symbols].dropna()

        temp_df = (temp_df / temp_df.iloc[0] - 1) * 100
        temp_df = temp_df.reset_index()
        temp_df.columns.values[0] = 'date'

        temp_df_melted = temp_df.melt(id_vars='date', var_name='symbol', value_name='price_perc_change')
        temp_df_melted['pair'] = f"{symbol_pair[0]} vs {symbol_pair[1]}"

        data_combined.append(temp_df_melted)

    final_df = pd.concat(data_combined)
    return final_df

def sma_data_prep(df: pd.DataFrame, symbols: list, n: int = 200, n_std : int = 2) -> dict:

    combined_dict = {}

    for symbol in symbols:

        prices = df[symbol].dropna()

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

