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
import os

# "mongodb+srv://sarabarrows18:mongo@cluster0.vgo9y.mongodb.net/"
# mango=os.environ.get(mongo_creds)
# client = pymongo.MongoClient(mango
#     )



# db = client["test-db"]
# # Go into one of my database's collection (table)
# collection = db["table"]


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
        
        # record = {
        #     "employee": input_val,
        #     "department": "engineering",
        #     "product": "PC",
        #     "part": "motherboard",
        #     "quantity": "12",
        #     "day": "Saturday"
        # }

        # collection.insert_one(record)
        # testing = collection.find_one()


        return f'{input_val} has been entered'
    return ''


# if __name__ == '__main__':
#     app.run_server(debug=True)
  