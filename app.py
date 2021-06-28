from financeapi import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from urllib.request import urlopen
import plotly.graph_objects as go
from dash.dependencies import Output, Input
from os import name

# with open('secretkey.txt') as f:
#     key = f.read()

# f = FinanceAPI()
# f.registerKey_(key)
# apple_dict = f.build_dict('AAPL')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Financial Valuation Dashboard: Understand companie's value"

app.layout = html.Div(
    children=[
        ### Header  ###
        html.Div(
            children=[
                html.H1(
                    children="Valuation Dashboard", className='header-title'
                ),
                html.P(
                    children="Analyze stocks based on quantitative factors",
                    className='header-description'
                )
            ],
            className='header'
        ),
        ### Stock input ####
        html.Div(
            children=[
                dcc.Input(className="Stock-Input", type="text", id='stock-search', placeholder='AAPL'),
                html.Button('Submit', className='button')
            ],
            className='menu'
        ),
        #Company info
        html.Div(
            children=[
                html.H2(children="🍎",
                        className='logo'),
                html.H2(children='Apple Corporation', className='company-name'),
                html.H2(children='(AAPL)', className='company-ticker'),
                html.H2(children='$130.76', className='company-price'),
                html.H3(children='2.70', className='price-change'),
                html.H3(children='(-1.01%)', className='price-change')

            ],
            className="company-info"
        ),
        #Financial Summary
        html.Div(
            children=[
                html.Table(
                    children=[
                        html.Tbody(
                            children=[
                                html.Tr(
                                    children=[
                                        html.Th(children='Symbol', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['symbol']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Price', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        html.Td(children='X.XX%', className='summary-data'),                                        
                                        #html.Td(children=f"{apple_dict['profile']['price']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Beta', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['beta']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Volume Avg.', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['volAvg']}") 
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Market Cap', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['mktCap']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Last Dividend', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['lastDiv']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='52 wk range', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['profile']['range']}")
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                html.Table(
                    children=[
                        html.Tbody(
                            children=[
                                html.Tr(
                                    children=[
                                        html.Th(children='ROE', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['returnOnEquity']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='ROA', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['returnOnAssets']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Operating Margin', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['operatingProfitMargin']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='Debt/Equity', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['debtEquityRatio']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='P/E', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['priceEarningsRatio']}")
                                    ]
                                ),
                                html.Tr(
                                    children=[
                                        html.Th(children='P/B', scope='row'),
                                        html.Td(children='data', className='summary-data'),
                                        #html.Td(children=f"{apple_dict['ratios']['priceToBookRatio']}")
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ],
            className="financial-summary card"
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id='price-chart', config={'displayModeBar': False},
                    ),
                    className='card'
                ),
                html.Div(
                    children=dcc.Graph(
                        id='earnings-chart', config={'displayModeBar': False},
                    ),
                    className='card'
                ),
            ],
            className='wrapper',
        ),
    ],
    className='main-div'
)

@app.callback(
    #define output objects
    [
        Output('price-chart', 'figure'),
        Output('volume-chart', 'figure')
    ],
    #define input objects (elem waiting for changes, property of elements)
    [
        Input('stock-search', 'value')
    ]
)

def request_stock_info():
    pass

@app.callback(
    #define output objects
    [
        Output('price-chart', 'figure'),
        Output('volume-chart', 'figure')
    ],
    #define input objects (elem waiting for changes, property of elements)
    [
        Input('stock-search', 'value')
    ]
)

def update_dashboard():
    pass

if __name__ == '__main__':
    app.run_server(debug=True)