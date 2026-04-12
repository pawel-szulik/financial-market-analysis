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

def heatmap_corr(df: pd.DataFrame) -> None:
    sns.heatmap(df,
                cmap="coolwarm",
                center=0,
                vmin=-1,
                vmax=1)
