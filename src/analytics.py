import pandas as pd
import scipy.stats as stats

def correlations(df: pd.DataFrame, corr_type: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes a table of selected correlation coefficients along with their p-values.
    :param df: pd.DataFrame
    :param corr_type: str
    :return: tuple[pd.DataFrame, pd.DataFrame]
    """
    cols = df.columns
    corrs = pd.DataFrame(index=cols, columns=cols, dtype=float)
    p_vals = pd.DataFrame(index=cols, columns=cols, dtype=float)

    for idx_i, i in enumerate(cols):
        for idx_j, j in enumerate(cols):
            if idx_j < idx_i:
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

    return corrs, p_vals


def regression(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes a table of linear regression slope coefficients and p-value significance tests.
    :param df: pd.DataFrame
    :return: tuple[pd.DataFrame, pd.DataFrame]
    """

    cols = df.columns
    slopes = pd.DataFrame(index=cols, columns=cols, dtype=float)
    p_vals = pd.DataFrame(index=cols, columns=cols, dtype=float)

    for i in cols:
        for j in cols:

            valid = df[[i, j]].dropna()
            x = valid[i].values
            y = valid[j].values

            reg = stats.linregress(x, y)

            slopes.loc[i, j] = reg.slope
            p_vals.loc[i, j] = reg.pvalue

    return slopes, p_vals