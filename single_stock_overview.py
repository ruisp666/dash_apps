import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output

# A bit of style
import dash_bootstrap_components as dbc

from fmp_extractor.news.news import extract_top_news
from aux import get_names_symbols, graph_callback_all_history, graph_callback_high_freq

# List of options for tickers based on the list of available symbols
names_symbols = get_names_symbols()


# Values to compute the averages of the means
SHORT_TERM = 30
LONG_TERM = 200

# Alert text
alert_text = 'Data not available for the specified security, please change.'
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[html.Div(className='row', children=[
    html.H4('Closing price'),
    html.Div(className='row', children=[
        dcc.Dropdown(
            id='name_1',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
        ),
        dcc.Graph(id='close_price_1')], style={'display': 'inline-block', 'width': '48%', 'height': '50%'}),
    html.Div(children=[
        dcc.Dropdown(
            id='name_3',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
        ),
        html.Div(id='raise_not_available', children=[]),
        dcc.Graph(id='close_price_3')], style={'display': 'inline-block', 'width': '48%', 'height': '700'}),
        ]),
        html.H4(children='News'),
        html.Div(id='no_news', children=[], style={'width': '3', 'height': '15'}),
        html.Div(className='row', children=[
            html.Div(id='news')],
                 style={'display': 'inline-block', 'width': '100%', 'height': '700'})
])


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


@app.callback(Output('close_price_3', 'figure'),
              Output('raise_not_available', 'children'),
               Input('name_3', 'value'))
def price_hist_3(name_3):
    close_figure = graph_callback_high_freq(name_3, names_symbols, freq='1min', short_term=SHORT_TERM,
                                            long_term=LONG_TERM)
    if close_figure is None:
        return dash.no_update, dbc.Alert(alert_text, color='danger', dismissable=True)
    close_figure.update_layout(height=700, yaxis=dict(autorange=True, fixedrange=False),
                               xaxis=dict(
                                   rangeselector=dict(
                                       buttons=list([
                                           dict(count=60,
                                                label="1h",
                                                step="minute",
                                                stepmode="backward"),
                                           dict(count=240,
                                                label="4h",
                                                step="minute",
                                                stepmode="backward"),
                                           dict(count=7,
                                                label="1d",
                                                step="hour",
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

    return close_figure, dash.no_update


@app.callback(Output('news', 'children'),
              Output('no_news', 'children'),
                Input('name_3', 'value'))
def generate_table(name):
    ticker = names_symbols.at[name, 'symbol']
    news = extract_top_news([ticker], limit=20)
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
                # html.Td(df.iloc[i]['text'])
            ]) for i in range(df.shape[0])])
    ])
    return dbc.Table(table, bordered=True, striped=True, responsive=True, color='light',
                     style={'white-space': 'nowrap',  'border-spacing': '3px'}), dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
