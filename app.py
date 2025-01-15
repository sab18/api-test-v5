import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

# import gspread
# from google.oauth2.service_account import Credentials

# import json
# import os
# from dotenv import load_dotenv



# #LOCAL or DEPLOY
# source='DEPLOY'   


# if source=='LOCAL':
#     credentials='CREDENTIALS_JSON_LOCAL'
#     credentials_path='src/credentials.json'
# elif source=='DEPLOY':
#     credentials='CREDENTIALS_JSON_DEPLOY'
#     credentials_path='credentials.json'


# load_dotenv()
# credentials_json = os.environ.get(credentials)

# if credentials_json:
#     with open(credentials_path, "w") as f:
#         f.write(credentials_json)
# else:
#     raise ValueError("CREDENTIALS_JSON environment variable is not set")



# scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# creds = Credentials.from_service_account_file(credentials_path,scopes=scopes)

# client = gspread.authorize(creds)
# sheet_id = "1Xp3jzJsTYeyJ5dE-uqeB0soCpsEFic2FgQvSO4JJ3zk"


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
                
        # sheet = client.open_by_key(sheet_id).sheet1
        # sheet.append_row([input_val,2])
        # #sheet.update_cell(1, 1, input_val)
        

        return f'{input_val} has been entered'
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)