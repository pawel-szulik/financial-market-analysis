import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

sns.set_style("whitegrid")

def price_percentage_change_comparison(df: pd.DataFrame, combinations: list) -> None:
    """
    Creates a plot, consisting of many subplots comparing different financial instruments and their price percentage changes over time.
    :param df: prepared dataframe
    :param combinations: list of tuples with two symbols
    :return: None
    """
    data_combined = []

    for symbol_pair in combinations:
        temp_df = df.xs('close', axis=1, level=1)[list(symbol_pair)]

        temp_df_perc = ((temp_df - temp_df.iloc[0]) / temp_df.iloc[0]) * 100
        temp_df_perc=temp_df_perc.reset_index()

        temp_df_melted = temp_df_perc.melt(id_vars='date', var_name='symbol', value_name='price_perc_change')
        temp_df_melted['pair'] = f"{symbol_pair[0]} vs {symbol_pair[1]}"

        data_combined.append(temp_df_melted)

    final_df = pd.concat(data_combined)

    g = sns.relplot(data=final_df, kind='line',
                    x='date', y='price_perc_change',
                    hue='symbol', col = 'pair',
                    col_wrap=3, facet_kws={'sharey': False},
    )

    g = (g.set_axis_labels("Date", "Price change (%)"))
    g = (g.set_titles(template="Comparison: {col_name}", size=14))



def price_change_distributions(df: pd.DataFrame) -> None:
    sns.pairplot(df,
                 kind="reg",
                 plot_kws={
                     "scatter_kws": {"s": 3, "alpha": 0.6, "color": "#4DA3FF"},
                     "line_kws": {"color": "red", "linewidth": 1}},
                 diag_kws={"edgecolor":"none", "linewidth":0, "alpha":1})


def heatmap_corr(df: pd.DataFrame) -> None:
    sns.heatmap(df,
                cmap="RdBu_r",
                center=0,
                vmin=-1,
                vmax=1)

def highlight_significant(pvals: pd.DataFrame):
    """
    Marks significant results at the 5% level in given DataFrame.
    """
    def styler(df_values: pd.DataFrame):
        mask = pvals < 0.05

        return pd.DataFrame(
            np.where(mask, "background-color: red", ""),
            index=df_values.index,
            columns=df_values.columns
        )
    return styler