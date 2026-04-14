import pandas as pd

def investment_strategy_sim(close_prices: pd.DataFrame, symbols: list, monthly_investment_pln: float = 500.0, start_date: str='2024-10-01') -> pd.DataFrame:

    summary_table = []

    for symbol in symbols:

        prices = close_prices[symbol].loc[start_date:].dropna()
        currency_exchange_rates = close_prices['USDPLN'].loc[start_date:].dropna()

        purchase_dates = prices.resample('BMS').first().index

        total_units_bought = 0
        total_money_invested = 0

        for date in purchase_dates:
            current_unit_price = prices.asof(date)
            current_USDPLN_rate = currency_exchange_rates.asof(date)

            monthly_investment_usd = monthly_investment_pln / current_USDPLN_rate
            units_bought = monthly_investment_usd / current_unit_price

            total_units_bought += units_bought
            total_money_invested += monthly_investment_pln

        final_price_usd = prices.iloc[-1]
        final_USDPLN_rate = currency_exchange_rates.asof(prices.index[-1])

        total_investment_value = total_units_bought * final_price_usd * final_USDPLN_rate
        total_profit = total_investment_value - total_money_invested
        total_profit_perc = (total_investment_value - total_money_invested) / total_money_invested * 100

        summary_table.append({
            'symbol': symbol,
            'Total invested PLN': total_money_invested,
            'Final investment value': round(total_investment_value, 2),
            'Final profit': round(total_profit, 2),
            'Final profit_perc': round(total_profit_perc, 2),
        })

    return pd.DataFrame(summary_table).sort_values(by='Final profit_perc', ascending=False)

