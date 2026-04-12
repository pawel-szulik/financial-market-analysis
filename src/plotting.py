import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import seaborn as sns
from data_loader import DataManager

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


def price_change_plots_2_symbols(df: pd.DataFrame, combinations: list) -> None:
    """
    Draws scatter plots of the price changes of two symbols for the given combinations.
    Then, it adds a regression line. The plots are saved to a PDF file.
    :param df: prepared dataframe
    :param combinations: list of tuples with two symbols
    :return: None
    """
    output_file = "price_change_plots_2_symbols.pdf"

    with PdfPages(output_file) as pdf:
        for combination in combinations:
            x = df[(combination[0], "perc_change")]
            y = df[(combination[1], "perc_change")]

            # Trend line ------------------------------------
            coef = np.polyfit(x, y, 1)
            func = np.poly1d(coef)

            x_range = np.linspace(x.min(), x.max(), 100)

            # Plot ------------------------------------------

            plt.figure(figsize=(10, 6))

            plt.scatter(x, y, s=10, alpha=0.3, color='blue', label='Percent price changes')
            plt.plot(x_range, func(x_range), color="red", linewidth=2, label=f"Trend (slope: {coef[0]:.2f})")

            plt.xlabel(f"Change for {combination[0]}")
            plt.ylabel(f"Change for: {combination[1]}")
            plt.title(f"{combination[0]} vs {combination[1]}")
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            pdf.savefig()
            plt.close()

        print(f"Plots saved to: {output_file}")
