from dash import Dash, dash_table, dcc, html, Input, Output

# A bit of style
import dash_bootstrap_components as dbc
from aux import get_names_symbols, get_all_quotes

# List of options for tickers based on the list of available symbols
names_symbols = get_names_symbols()
exchanges = names_symbols.exchange.unique()

# Order of the columns to show in the table
order_column = ['name', 'symbol', 'changesPercentage', 'marketCap', 'volume', 'voltoavgvolume',  'price',  'change', 'dayLow',
                      'dayHigh', 'yearHigh', 'yearLow',   'priceAvg50',
                      'priceAvg200', 'exchange', 'open',
                      'previousClose', 'eps', 'pe', 'earningsAnnouncement',
                      'sharesOutstanding', 'timestamp']
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[
    html.H4("Market view"),
    dcc.Dropdown(
        id='exchange',
        value='XETRA',
        clearable=True,
        options=exchanges
    ),
    html.Div(id='table')
])


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
        page_current= 0,
        page_size= 20,
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


if __name__ == '__main__':
    app.run_server(debug=True, port=8070)

