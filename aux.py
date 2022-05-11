import urllib

import pandas as pd
import numpy as np
from fmp_extractor.config import API_KEY
from fmp_extractor.prices.historic import extract_prices_history, extract_prices_high_frequency
from fmp_extractor.prices.live import extract_prices_batch
import plotly.express as px
from functools import partial


update = False
if update is True:
    LIST_SYMBOLS = pd.read_json(f'https://financialmodelingprep.com/api/v3/available-traded/list?apikey={API_KEY}')
    LIST_SYMBOLS.to_pickle('list_tradable_symbols.pickle')
    print('List updated')
else:
    LIST_SYMBOLS = pd.read_pickle('list_tradable_symbols.pickle')


def get_names_symbols(list_symbols=LIST_SYMBOLS):
    names_symbols = list_symbols.loc[:, ['name', 'symbol', 'exchange']]
    names_symbols.loc[:, 'name_symbol'] = names_symbols.loc[:, 'name'] + ', ' + names_symbols.loc[:, 'symbol']
    names_symbols.set_index('name_symbol', inplace=True)
    return names_symbols


def get_prices(extract_type: str, ticker: str, freq=None):
    if extract_type == 'all':
        prices = extract_prices_history([ticker], start_date='beginning')
        return prices.pivot(values='close', columns='symbol', index='date')
    if extract_type == 'high_freq':
        try:
            prices =  extract_prices_high_frequency(ticker, freq=freq)
        except KeyError:
            return None
        return prices.set_index('date').loc[:, 'close'].to_frame(name=ticker).asfreq(freq)


def graph_callback(name, names_symbols, short_term, long_term, extract_type, freq):
    ticker = names_symbols.at[name, 'symbol']
    close = get_prices(extract_type, ticker, freq)
    if close is None:
        return None
    else:
        st_close = close.rolling(f'{short_term}d').mean()
        lt_close = close.rolling(f'{long_term}d').mean()
        stocks = pd.concat([close[ticker], st_close[ticker], lt_close[ticker]], axis=1,
                       keys=['close', f'{short_term}d-MA', f'{long_term}d-MA'])
        close_fig = px.line(stocks, y=stocks.columns, x=stocks.index)
    return close_fig


graph_callback_all_history = partial(graph_callback, extract_type='all')
graph_callback_high_freq = partial(graph_callback, extract_type='high_freq')


def get_all_quotes(exchange: str):
    tickers_to_extract = LIST_SYMBOLS.loc[LIST_SYMBOLS.exchange == exchange, 'symbol'].values
    len_exchange = len(tickers_to_extract)
    if len_exchange < 1500:
        return extract_prices_batch(tickers_to_extract)
    else:
        print('Updating 1500 tickers per request')
        n_batches = np.ceil(len_exchange / 1500)
        arrays = np.array_split(tickers_to_extract, n_batches)
        # Using np.vectorize here does not work quite efficiently, since the splits are ragged
        while True:
            try:
                frame = [extract_prices_batch(t) for t in arrays]
                break
            except urllib.error.HTTPError:
                print('Increasing the size of the batches')
                n_batches += 1
                arrays = np.array_split(tickers_to_extract, n_batches)
        return pd.concat(frame)


if __name__ == '__main__':
    df = get_all_quotes('New York Stock Exchange')