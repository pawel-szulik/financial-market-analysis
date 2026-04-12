import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from .data_loader import DataManager

sns.set_style("darkgrid")

def comparison_plot(dm: DataManager, combinations: list) -> None:

    final_df = dm.comparison_df_prep(combinations)

    g = sns.relplot(data=final_df, kind='line',
                    x='date', y='price_perc_change',
                    hue='symbol', col = 'pair',
                    col_wrap=3, facet_kws={'sharey': False, 'sharex': False}
    )
    for ax in g.axes.flat:
        title = ax.get_title()
        if "BTCUSD" in title:
            ax.set_yscale('symlog')
            ax.set_ylabel("Price change % (log scale)")
        else:
            ax.set_yscale('linear')
            ax.set_ylabel("Price change % (linear scale)")

    g.set_axis_labels("Date")
    g.set_titles(template="{col_name}", size=14)

    add_market_events(g)

    plt.tight_layout()


def add_market_events(g: sns.FacetGrid) -> None:
    # test events - more to be added
    events = {'2020-02-24': 'Covid-19',
              '2022-02-24': "Ukraine's invasion",
              '2025-04-09': "USA tariffs on China"}

    for ax in g.axes.flat:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        for date, label in events.items():
            event_date = pd.to_datetime(date)
            event_num = mdates.date2num(event_date)
            if xmin <= event_num <= xmax:
                ax.axvline(x=event_date, color='red', linestyle="--", alpha=0.5)
                ax.text(event_date, ymax, label, rotation=90, color='darkred', ha='right', va='top', bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

def price_change_distributions(df: pd.DataFrame) -> None:
    sns.pairplot(df,
                 kind="reg",
                 plot_kws={
                     "scatter_kws": {"s": 3, "alpha": 0.5, "color": "#4DA3FF"},
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