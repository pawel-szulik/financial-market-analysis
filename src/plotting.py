import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates
import seaborn as sns

sns.set_style("darkgrid")

def comparison_df_prep(df: pd.DataFrame, combinations: list) -> pd.DataFrame:
    """
    Prepares a df for plotting the comparison.
    :param df: specified dataframe
    :param combinations: list of tuples with two symbols (of financial instruments)
    :return: pd.DataFrame -
    """
    data_combined = []

    for symbol_pair in combinations:
        found_symbols = [s for s in symbol_pair if s in df.columns]

        temp_df_perc = df[found_symbols].copy()
        temp_df_perc = temp_df_perc.dropna()

        temp_df_perc=temp_df_perc.reset_index()
        temp_df_perc.columns.values[0] = 'date'

        temp_df_melted = temp_df_perc.melt(id_vars='date', var_name='symbol', value_name='price_perc_change')
        temp_df_melted['pair'] = f"{symbol_pair[0]} vs {symbol_pair[1]}"

        data_combined.append(temp_df_melted)

    final_df = pd.concat(data_combined)
    return final_df

def comparison_plot(df: pd.DataFrame, combinations: list) -> None:

    final_df = comparison_df_prep(df, combinations)

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
    g.set_titles(template="Comparison: {col_name}", size=14)

    add_market_events(g)


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

