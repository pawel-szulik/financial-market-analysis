import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

from src.config import EVENTS
import src.analytics as aly

sns.set_theme(style="dark")

plt.rcParams.update({
    "figure.facecolor": "#161616",
    "axes.facecolor": "#161616",
    "savefig.facecolor": "#161616",

    "axes.edgecolor": "#cccccc",
    "axes.labelcolor": "#dddddd",

    "xtick.color": "#cccccc",
    "ytick.color": "#cccccc",

    "text.color": "#dddddd",
    "axes.titlecolor": "#dddddd",
    "axes.titleweight": "bold",

    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": True,
    "axes.spines.bottom": True,

    "legend.edgecolor": "none",
    "legend.framealpha": 0,
    "legend.labelcolor": "#dddddd",
    })

def add_market_events(ax, xmin, xmax, ymax) -> None:
    for date, label in EVENTS.items():
        event_date = pd.to_datetime(date)
        event_num = mdates.date2num(event_date)

        if xmin <= event_num <= xmax:
            ax.axvline(x=event_date,
                       color='white',
                       linestyle="--",
                       alpha=0.5,
                       linewidth=1)
            ax.text(event_date - pd.Timedelta(days=30),
                    ymax,
                    label,
                    rotation=90,
                    color='#ef9a9a',
                    ha='right',
                    va='top',
                    size=10,
                    bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', pad=1))


def rolling_volatility_plot(df: pd.DataFrame, window: int) -> None:
    temp = df.rolling(window).var(ddof=0).pow(0.5)

    ax = sns.lineplot(data=temp, dashes=False, linewidth=0.7)
    ax.legend(loc='upper left', bbox_to_anchor=(0.9, 1))
    ymax = temp.max().max()
    xmin, xmax = ax.get_xlim()

    add_market_events(ax, xmin, xmax, ymax)


def comparison_plot(df: pd.DataFrame, combinations: list) -> None:

    final_df = aly.comparison_df_prep(df, combinations)

    g = sns.relplot(data=final_df, kind='line',
                    x='date', y='price_perc_change',
                    hue='symbol', col = 'pair', linewidth=0.7,
                    palette="deep",
                    col_wrap=3,
                    facet_kws={'sharey': False, 'sharex': False}
    )
    for ax in g.axes.flat:
        title = ax.get_title()
        if "Bitcoin" in title:
            ax.set_yscale('symlog')
            ax.set_ylabel("Price change % (log scale)")
            ax.set_ylim(-100)
        else:
            ax.set_yscale('linear')
            ax.set_ylabel("Price change % (linear scale)")

    g.set_axis_labels("Date")
    g.set_titles(template="{col_name}", size=14)


def sma_change_plot(df: pd.DataFrame, symbols: list) -> None:
    df_dict = aly.sma_data_prep(df, symbols)
    for symbol, df in df_dict.items():
        date = df.columns[0]
        df['date'] = pd.to_datetime(df[date])
        df = df.sort_values(by=['date'])

        # lower_band shape fix
        df['lower_band'] = np.where(df['lower_band'] < df['sma'] * 0.2,
                                    df['sma'] * 0.2,
                                    df['lower_band'])

        plt.figure(figsize=(10, 5))

        ax=sns.lineplot(data=df,x=date, y='sma', color='#E2B05E', linewidth=1.5, label = 'SMA')
        sns.lineplot(data=df,x=date, y='price', color='white', alpha=0.3, linewidth=0.3, label = 'Price')
        sns.lineplot(data=df, x=date, y='lower_band', color ='#CD5C5C', linestyle='--', label = 'Lower band')
        sns.lineplot(data=df, x=date, y='upper_band', color='#556B2F', linestyle='--', label = 'Upper band')

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        add_market_events(ax, xmin, xmax, ymax)

        title = f"{symbol}'s Simple Moving Average"

        if "Bitcoin" in symbol:
            plt.yscale('log')
            title = f"{symbol}'s Simple Moving Average (log scale)"
            plt.ylabel("Price (log scale)")
        else:
            plt.ylabel("Price")

        plt.xlabel("Date")
        plt.title(title)
        plt.legend(loc='lower right')
        plt.show()

def price_change_distributions(df: pd.DataFrame) -> None:
    sns.pairplot(df,
                 plot_kws={"s": 3, "alpha": 0.5, "color": "#2C6A8A"},
                 diag_kws={"edgecolor":"none", "linewidth":0, "alpha":1, "color":"#2C6A8A"})


def heatmap_corr(df: pd.DataFrame, highlight: list[str] = None) -> None:
    cmap = LinearSegmentedColormap.from_list(
        "custom_dark",
        ["#3A7BD5", "black", "#E05A5A"]
    )
    cmap.set_bad("#B89B5E")

    mask = np.eye(df.shape[0], dtype=bool)

    plt.figure(figsize=(10, 8))

    ax = sns.heatmap(df,
                mask=mask,
                cmap=cmap,
                center=0,
                vmin=-1,
                vmax=1)

    highlight = set(highlight or [])

    # bold for the x-axis
    for label in ax.get_xticklabels():
        if label.get_text() in highlight:
            label.set_fontweight("bold")
            label.set_color("#FFF9C4")

    # bold for the y-axis
    for label in ax.get_yticklabels():
        if label.get_text() in highlight:
            label.set_fontweight("bold")
            label.set_color("#FFF9C4")


def highlight_significant(pvals: pd.DataFrame, lvl: float = 0.05):
    """
    Marks significant results at the 5% level in given DataFrame.
    """
    def styler(df_values: pd.DataFrame):
        mask = pvals < lvl

        return pd.DataFrame(
            np.where(mask, "background-color: #8C4F4F", "background-color: #2B2B2B"),
            index=df_values.index,
            columns=df_values.columns
        )
    return styler