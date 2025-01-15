import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from flask import Flask, request
import json

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

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
        # Save input_val to server
        with open('data.txt', 'a') as f:
            f.write(f'{input_val}\n')
        return f'{input_val} has been entered'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)