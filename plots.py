import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def price_linear_plots_2_symbols(df: pd.DataFrame, combinations: list) -> None:
    """
    Draws linear plots of the selected financial combinations of the given symbols.
    Saves the plots to a PDF file.
    """
    output_file = "price_linear_plots_2_symbols.pdf"
    with PdfPages(output_file) as pdf:
        for symbol in combinations:
            x = df.index
            y_1 = df[(symbol[0], "close")] / df[(symbol[0], "close")].iloc[0] * 100
            y_2 = df[(symbol[1], "close")] / df[(symbol[1], "close")].iloc[0] * 100

            fig, ax = plt.subplots(figsize=(10, 6))



            ax.set_xlabel("Date")
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.6)

            pdf.savefig()
            ax.clear()

        print(f"Plots saved to: {output_file}")


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


if __name__ == "__main__":
    main_df = pd.read_csv("prepared_data.csv", header=[0, 1], index_col=0, parse_dates=True)
    main_df = main_df.iloc[1:] # first row with NaNs omitted


    # example
    price_change_plots_2_symbols(main_df, combinations=[('GCUSD', '^GSPC'),
                                                        ('SIUSD', '^GSPC'),
                                                        ('BZUSD', '^GSPC'),
                                                        ('EURUSD', '^GSPC'),
                                                        ('BTCUSD', '^GSPC'),
                                                        ('ETHUSD', '^GSPC')
                                                        ])

    price_linear_plots_2_symbols(main_df, combinations=[('GCUSD', '^GSPC'),
                                                        ('SIUSD', '^GSPC'),
                                                        ('BZUSD', '^GSPC'),
                                                        ('EURUSD', '^GSPC'),
                                                        ('BTCUSD', '^GSPC'),
                                                        ('ETHUSD', '^GSPC')
                                                        ])