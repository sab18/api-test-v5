import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pymongo  
import plotly.express as px
import dash                                                     # pip install dash  (2.1 or higher)
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd                                             # pip install pandas
import plotly.express as px
import pymongo                                                  # pip install "pymongo[srv]"
from bson.objectid import ObjectId
# import gspread
# from google.oauth2.service_account import Credentials

# import json
# import os
# from dotenv import load_dotenv

client = pymongo.MongoClient(
    "mongodb+srv://sarabarrows18:mongo@cluster0.vgo9y.mongodb.net/")
# test the connection
# db = client.test
# print(db)
# exit()


db = client["test-db"]
# Go into one of my database's collection (table)
collection = db["table"]

# print(collection)


# record = {
#     "employee": "Mike",
#     "department": "engineering",
#     "product": "PC",
#     "part": "motherboard",
#     "quantity": "12",
#     "day": "Saturday"
# }

# collection.insert_one(record)
# testing = collection.find_one()
# print(testing)
# exit()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
server=app.server

app.layout = html.Div([
    html.H1('Web Application connected to a Live Database', style={'textAlign': 'center'}),
    # interval activated once/week or when page refreshed
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),

    html.Div([
        html.Div(id='pie-graph', className='five columns'),
        html.Div(id='hist-graph', className='six columns'),
    ], className='row'),
    dcc.Store(id='changed-cell')
])


# Display Datatable with data from Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find()))
    # Convert id from ObjectId to string so it can be read by DataTable
    df['_id'] = df['_id'].astype(str)
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'id': p, 'name': p, 'editable': False} if p == '_id'
                     else {'id': p, 'name': p, 'editable': True}
                     for p in df],
        ),
    ]


# store the row id and column id of the cell that was updated
app.clientside_callback(
    """
    function (input,oldinput) {
        if (oldinput != null) {
            if(JSON.stringify(input) != JSON.stringify(oldinput)) {
                for (i in Object.keys(input)) {
                    newArray = Object.values(input[i])
                    oldArray = Object.values(oldinput[i])
                    if (JSON.stringify(newArray) != JSON.stringify(oldArray)) {
                        entNew = Object.entries(input[i])
                        entOld = Object.entries(oldinput[i])
                        for (const j in entNew) {
                            if (entNew[j][1] != entOld[j][1]) {
                                changeRef = [i, entNew[j][0]] 
                                break        
                            }
                        }
                    }
                }
            }
            return changeRef
        }
    }    
    """,
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)


# Update MongoDB and create the graphs
@app.callback(
    Output("pie-graph", "children"),
    Output("hist-graph", "children"),
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if cc is None:
        # Build the Plots
        pie_fig = px.pie(tabledata, values='quantity', names='day')
        hist_fig = px.histogram(tabledata, x='department', y='quantity')
    else:
        print(f'changed cell: {cc}')
        print(f'Current DataTable: {tabledata}')
        x = int(cc[0])

        # update the external MongoDB
        row_id = tabledata[x]['_id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        collection.update_one({'_id': ObjectId(row_id)},
                              {"$set": {col_id: new_cell_data}})
        # Operations guide - https://docs.mongodb.com/manual/crud/#update-operations

        pie_fig = px.pie(tabledata, values='quantity', names='day')
        hist_fig = px.histogram(tabledata, x='department', y='quantity')

    return dcc.Graph(figure=pie_fig), dcc.Graph(figure=hist_fig)


if __name__ == '__main__':
    app.run_server(debug=False)

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


# app=dash.Dash(__name__)
# server=app.server

# app.layout = html.Div(
#     [
#         dcc.Input(placeholder='Write name here', id='input-val'),
#         html.Button('submit', id='button-id', n_clicks=0),
#         html.Div(id='output-val')
#     ]
# )


# @app.callback(
#     Output('output-val', 'children'),
#     Input('button-id', 'n_clicks'),
#     State('input-val', 'value')
# )
# def callbk(n_clicks, input_val):
    
#     if n_clicks > 0 and input_val:
                
#         # sheet = client.open_by_key(sheet_id).sheet1
#         # sheet.append_row([input_val,2])
#         # #sheet.update_cell(1, 1, input_val)
        

#         return f'{input_val} has been entered'
#     return ''


# if __name__ == '__main__':
#     app.run_server(debug=True)