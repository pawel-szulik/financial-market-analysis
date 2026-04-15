CATEGORIES = {"commodities": ('historical-price-eod/full', ['BZUSD', 'SIUSD', 'GCUSD']),
           "forex": ('historical-price-eod/full', ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'USDCAD', 'USDCNH', 'USDRUB', 'USDPLN']),
           "crypto": ('historical-price-eod/full', ['BTCUSD', 'ETHUSD', 'USDTUSD', 'USDCUSD', 'SOLUSD', 'XRPUSD', 'BNBUSD']),
           "indexes": ('historical-price-eod/full', ['^GSPC', '^DJI', '^IXIC', '^RUT', '^FTSE', '^N225', '^HSI', '^STOXX50E', '^VIX'])}

NAMES = {
    'BZUSD': "Brent Crude Oil",
    'SIUSD': "Silver",
    'GCUSD': "Gold",
    'EURUSD': "EURUSD",
    'USDJPY': "USDJPY",
    "GBPUSD": "GBPUSD",
    'USDCHF': "USDCHF",
    'USDCAD': "USDCAD",
    'USDCNH': "USDCNH",
    'USDRUB': "USDRUB",
    'USDPLN': "USDPLN",
    'BTCUSD': "Bitcoin",
    'ETHUSD': "Ethereum",
    'USDTUSD': "Tether",
    'USDCUSD': "USD Coin",
    'SOLUSD': "Solana",
    'XRPUSD': "XRP",
    'BNBUSD': "Binance Coin",
    '^GSPC': "S&P 500",
    '^DJI': "Dow Jones",
    '^IXIC': "NASDAQ",
    '^RUT': "Russell 2000",
    '^FTSE': "FTSE 100",
    '^N225': "Nikkei 225",
    '^HSI': "Hang Seng Index",
    '^STOXX50E': "EURO STOXX 50",
    '^VIX': "VIX"
}

# events - more to be added
EVENTS = {'2000-03-10':'Dot-com bubble burst',
          '2001-09-11':'9/11 attacks',
          '2008-09-15':'2008 financial crisis',
          '2013-11-29':"Bitcoin's first $1k",
          '2010-05-02':'EU debt crisis',
          '2014-11-27':"Oil's crash",
          '2018-03-22':'US-China Trade War',
          '2020-03-12':'Covid-19',
          '2022-02-24':'Russian Invasion',
          }

# Commodities (Towary i Surowce)
# BZUSD – Brent Crude Oil (Ropa naftowa typu Brent)
# SIUSD – Silver (Srebro kwotowane w dolarach)
# GCUSD – Gold (Złoto kwotowane w dolarach)

# Forex (Pary walutowe)
# EURUSD – Euro / Dolar amerykański
# USDJPY – Dolar amerykański / Jen japoński
# GBPUSD – Funt szterling / Dolar amerykański
# USDCHF – Dolar amerykański / Frank szwajcarski
# USDCAD – Dolar amerykański / Dolar kanadyjski
# USDCNH – Dolar amerykański / Juan chiński (offshore)
# USDRUB – Dolar amerykański / Rubel rosyjski
# USDPLN – Dolar amerykański / Złoty polski

# Crypto (Kryptowaluty)
# BTCUSD – Bitcoin (Największa kryptowaluta)
# ETHUSD – Ethereum (Platforma smart kontraktów)
# USDTUSD – Tether (Stablecoin powiązany z dolarem)
# USDCUSD – USD Coin (Stablecoin regulowany)
# SOLUSD – Solana (Szybka sieć blockchain)
# XRPUSD – XRP (Token sieci Ripple)
# BNBUSD – Binance Coin (Token giełdy Binance)

# Indexes (Indeksy giełdowe)
# ^GSPC – S&P 500 (500 największych spółek w USA)
# ^DJI – Dow Jones Industrial Average (30 gigantów przemysłowych USA)
# ^IXIC – NASDAQ Composite (Indeks spółek technologicznych)
# ^RUT – Russell 2000 (Indeks małych spółek w USA)
# ^FTSE – FTSE 100 (100 największych spółek na giełdzie w Londynie)
# ^N225 – Nikkei 225 (Główny indeks giełdy w Tokio)
# ^HSI – Hang Seng Index (Główny indeks giełdy w Hongkongu)
# ^STOXX50E – EURO STOXX 50 (50 największych spółek strefy euro)
# ^VIX – CBOE Volatility Index (Indeks zmienności, tzw. "indeks strachu")