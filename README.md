# Financial Market Analysis

Analysis of selected financial instruments across major asset classes, including equity indices, commodities, cryptocurrencies, and the forex market.

## General Information

This project focuses on the analysis of selected financial instruments, including the S&P 500, EURO STOXX 50, gold, Brent crude oil, Bitcoin, and USD/PLN. Its primary objective is to identify and explore potential relationships between these assets and broader financial markets.  

The study also provides an overview of key characteristics of these instruments, such as the distribution of daily returns, volatility dynamics, and reactions to major market events. Particular attention is given to less commonly discussed aspects, including time-varying volatility and the longest drawdown (bear market) periods.  

As part of the concluding stage of the analysis, a simple investment strategy was simulated, and its performance was compared against the benchmark results.  

This project was undertaken as an opportunity to gain practical experience in financial data analysis using Python, as well as in visualizing market relationships and applying statistical methods to real-world datasets. A secondary motivation was a strong personal interest and curiosity in financial markets and quantitative analysis.  

## Technologies Used

- Python 3.12
- matplotlib
- numpy
- pandas
- seaborn
- scipy

## Features

- Loading and preprocessing of financial time series data
- Computation of descriptive statistics
- Correlation analysis (Pearson and Spearman) and linear regression modelling
- Statistical significance testing of results
- Standardized visualizations of prices, volatility, and moving averages, including annotations of key macroeconomic and geopolitical events
- Correlation heatmaps and return distribution histograms
- Analysis of the longest drawdown periods (time to recover to historical highs)
- Simulation and evaluation of a simple investment strategy with performance comparison

# Project Structure

```text
financial-market-analysis/
│
├── data/
│   ├── commodities/
│   ├── crypto/
│   ├── forex/
│   └── indexes/
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── analytics.py
│   ├── config.py
│   ├── data_loader.py
│   ├── investment_strategy_simulation.py
│   ├── plotting.py
│   └── __init__.py
│
├── README.md
└── requirements.txt
```

## Setup

The project requires Python 3.14.0. All dependencies can be installed using the provided requirements.txt file. 

```bash
pip install -r requirements.txt  
```

The analysis is located in the notebooks/analysis.ipynb Jupyter Notebook file, which can be executed to reproduce all computations and results presented in the project.

## Data Source

The data used in this analysis were obtained from Financial Modeling Prep and consist of daily price observations for selected financial instruments.
