from dash import Dash, dash_table, dcc, html, Input, Output
import dash
import pandas as pd
# A bit of style
import dash_bootstrap_components as dbc
from fmp_extractor.news.news import extract_top_news

from aux import get_names_symbols, get_all_quotes, graph_callback_all_history

# List of options for tickers based on the list of available symbols
names_symbols = get_names_symbols()
exchanges = names_symbols.exchange.unique()

# Values to compute the averages of the means
SHORT_TERM = 30
LONG_TERM = 200

# Order of the columns to show in the table
order_column = ['name', 'symbol', 'price', 'changesPercentage', 'price_to_yearHighpercent', 'marketCap', 'volume',
                'voltoavgvolume', 'change', 'dayLow',
                'dayHigh', 'yearHigh', 'yearLow',
                'priceAvg200', 'exchange', 'open',
                'previousClose', 'eps', 'pe', 'earningsAnnouncement',
                'sharesOutstanding', 'timestamp']
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(className='row', children=[
    html.Div(children=[
        html.H4("Market view"),
        dcc.Dropdown(
            id='exchange',
            value='XETRA',
            clearable=True,
            options=exchanges
        ),
        html.Div(id='table')]),
    html.Div(className='row', children=[ html.Div(className='row', children=[
        html.H4("Historical Chart"),
        dcc.Dropdown(
            id='name_1',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
        ),
        dcc.Graph(id='close_price_1')], style={'display': 'inline-block', 'width': '48%', 'height': '50%'}),
                                        html.Div(className='row', children=[
                                            html.H4("Latest News"),
                                            html.Div(children=html.Div(id='no_news', children=[],
                                                                       style={'width': '3', 'height': '15'})),
                                            html.Div(className='row', children=[html.Div(id='news')])],
                                                 style={'display': 'inline-block', 'width': '48%', 'height': '700'}
                                                 )]
             )]
)


@app.callback(Output('table', 'children'), Input('exchange', 'value'))
def get_quotes_exchange(exch):
    df = get_all_quotes(exch)
    df.loc[:, 'price_to_yearHighpercent'] = (df.loc[:, 'price'] /
                                             df.loc[:, 'yearHigh'] * 100).copy()
    df['marketCap'] *= 1e-9
    df['voltoavgvolume'] = df['volume'] / df['avgVolume']
    return dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i.capitalize(), "id": i, "deletable": True, "selectable": True} for i in df.loc[:, order_column]
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        virtualization=True,
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
        },
        style_table={'minWidth': '100%'},
        fixed_columns={'headers': True, 'data': 1},

    ),


@app.callback(Output('close_price_1', 'figure'), Input('name_1', 'value'))
def price_hist_1(name_1):
    close_figure = graph_callback_all_history(name_1, names_symbols, freq=None, short_term=SHORT_TERM,
                                              long_term=LONG_TERM)
    close_figure.update_layout(height=700, yaxis=dict(autorange=True, fixedrange=False),
                               xaxis=dict(
                                   rangeselector=dict(
                                       buttons=list([
                                           dict(count=1,
                                                label="1m",
                                                step="month",
                                                stepmode="backward"),
                                           dict(count=6,
                                                label="6m",
                                                step="month",
                                                stepmode="backward"),
                                           dict(count=1,
                                                label="YTD",
                                                step="year",
                                                stepmode="todate"),
                                           dict(count=1,
                                                label="1y",
                                                step="year",
                                                stepmode="backward"),
                                           dict(count=2,
                                                label="2y",
                                                step="year",
                                                stepmode="backward"),
                                           dict(count=5,
                                                label="5y",
                                                step="year",
                                                stepmode="backward"),
                                           dict(step="all")
                                       ])
                                   ),
                                   rangeslider=dict(
                                       visible=True
                                   ),
                                   type="date"
                               )
                               )
    return close_figure


@app.callback(Output('news', 'children'),
              Output('no_news', 'children'),
              Input('name_1', 'value'))
def generate_table(name):
    ticker = names_symbols.at[name, 'symbol']
    news = extract_top_news([ticker], limit=50)
    try:
        df = pd.DataFrame.from_records(list(news.values())[0]).loc[:, ['publishedDate', 'title', 'text', 'url']]
    except KeyError:
        return dash.no_update, dbc.Alert('No news for the selected ticker', color='danger', dismissable=True)

    df['Date'] = df['publishedDate'].str[:11]
    df['Time'] = df['publishedDate'].str[11:]
    table = html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in ['Date', 'Time', 'Title']],
                    style={'white-space': 'nowrap', 'padding': '3px'})
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i]['Date'], style={'white-space': 'nowrap', 'padding': '3px'}),
                html.Td(df.iloc[i]['Time'], style={'white-space': 'nowrap', 'padding': '3px'}),
                dcc.Link(html.A(df.iloc[i]['title']), href=df.iloc[i]['url'], target="_blank")
            ]) for i in range(df.shape[0])])
    ])
    return dbc.Table(table, bordered=True, striped=True, responsive=True, color='light',
                     style={'white-space': 'nowrap', 'border-spacing': '3px'}), dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, port=8070)
