import plotly.io as pio
from dash import Dash, dcc, html, Input, Output
from aux import get_names_symbols, graph_callback_all_history, graph_callback_high_freq

# List of options for tickers based on the list of available symbols
names_symbols = get_names_symbols()

# Template
pio.templates.default = "simple_white"

# Values to compute the averages of the means
SHORT_TERM = 15
LONG_TERM = 50

app = Dash(__name__)
app.layout = html.Div(children=[html.Div(className='row', children=[
    html.H4('Closing price'),
    html.Div(className='row', children=[
        dcc.Dropdown(
            id='name_1',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
        ),
        dcc.Graph(id='close_price_1')], style={'display': 'inline-block', 'width': '48%', 'height': '700'}),
    html.Div(children=[
        dcc.Dropdown(
            id='name_2',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
        ),
        dcc.Graph(id='close_price_2')], style={'display': 'inline-block', 'width': '48%', 'height': '700'}),

]),
    html.Div(className='row', children=[
        html.H4('High frequency price'),
        html.Div(className='row', children=[
            dcc.Dropdown(
            id='name_3',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
            ),
            dcc.Graph(id='close_price_3')], style={'display': 'inline-block', 'width': '48%', 'height': '700'}),
        html.Div(children=[
            dcc.Dropdown(
            id='name_4',
            value='Netflix, Inc., NFLX',
            clearable=True,
            options=names_symbols.index
            ),
            dcc.Graph(id='close_price_4')], style={'display': 'inline-block', 'width': '48%', 'height': '700'})]
            )
])


@app.callback(Output('close_price_1', 'figure'), Input('name_1', 'value'))
def price_hist_1(name_1):
    close_figure = graph_callback_all_history(name_1, names_symbols, freq=None, short_term=SHORT_TERM, long_term=LONG_TERM)
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


@app.callback(Output('close_price_2', 'figure'), Input('name_2', 'value'))
def price_hist_2(name_2):
    close_figure = graph_callback_all_history(name_2, names_symbols, freq=None, short_term=SHORT_TERM, long_term=LONG_TERM)
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


@app.callback(Output('close_price_3', 'figure'), Input('name_3', 'value'))
def price_hist_3(name_3):
    close_figure = graph_callback_high_freq(name_3,  names_symbols, freq='1min', short_term=SHORT_TERM, long_term=LONG_TERM)
    close_figure.update_layout(height=700, yaxis=dict(autorange=True, fixedrange=False),
                               xaxis=dict(
                                   rangeselector=dict(
                                       buttons=list([
                                           dict(count=12,
                                                label="1d",
                                                step="hour",
                                                stepmode="backward"),
                                           dict(count=2,
                                                label="2d",
                                                step="day",
                                                stepmode="backward"),
                                           dict(count=1,
                                                label="1d",
                                                step="day",
                                                stepmode="backward"),
                                           dict(count=10,
                                                label="2w",
                                                step="day",
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


@app.callback(Output('close_price_4', 'figure'), Input('name_4', 'value'))
def price_hist_4(name_4):
    close_figure = graph_callback_high_freq(name_4,  names_symbols, freq='1min', short_term=SHORT_TERM, long_term=LONG_TERM)
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
                                           dict(count=12,
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

    return close_figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
