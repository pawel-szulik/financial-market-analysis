import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from .data_loader import DataManager
from .config import EVENTS

sns.set_theme(style="dark")

def add_market_events(ax, xmin, xmax, ymax) -> None:
    for date, label in EVENTS.items():
        event_date = pd.to_datetime(date)
        event_num = mdates.date2num(event_date)

        if xmin <= event_num <= xmax:
            ax.axvline(x=event_date,
                       color='red',
                       linestyle="--",
                       alpha=0.5,
                       linewidth=1)
            ax.text(event_date,
                    ymax,
                    label,
                    rotation=90,
                    color='darkred',
                    ha='right',
                    va='top',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))


def rolling_volatility(df: pd.DataFrame) -> None:
    temp = df.rolling(100).var(ddof=0).pow(0.5)
    ax = sns.lineplot(data=temp, dashes=False)
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 1))
    ymax = temp.max().max()
    xmin, xmax = ax.get_xlim()

    add_market_events(ax, xmin, xmax, ymax)


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

    add_market_events_special(g)

    plt.tight_layout()


def add_market_events_special(g: sns.FacetGrid) -> None:
    for ax in g.axes.flat:
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        add_market_events(ax, xmin, xmax, ymax)


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