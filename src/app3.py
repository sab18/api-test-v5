import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import gspread
from google.oauth2.service_account import Credentials

import json
import os
from dotenv import load_dotenv





app=dash.Dash(__name__)
server=app.server

app.layout = html.Div(
    [
        dcc.Input(placeholder='Write name here', id='input-val'),
        html.Button('submit', id='button-id', n_clicks=0),
        html.Div(id='output-val')
    ]
)


@app.callback(
    Output('output-val', 'children'),
    Input('button-id', 'n_clicks'),
    State('input-val', 'value')
)
def callbk(n_clicks, input_val):
    
    if n_clicks > 0 and input_val:
                
        

        return f'{input_val} has been entered'
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)