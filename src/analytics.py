import pandas as pd
import scipy.stats as stats
import numpy as np

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