import dash
from dash import dcc, html, Input, Output, State
from datetime import datetime
import flask

# Server and app initialization
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

# In-memory dictionary to track user sessions (for demo purposes)
user_sessions = {}

app.layout = html.Div([
    dcc.Store(id='session-id', storage_type='local'),  # Unique session identifier
    html.Div(id='timer-output'),
    dcc.Interval(id='interval', interval=1000),  # Every second
    html.Script('''
        window.addEventListener('beforeunload', function () {
            fetch('/close', {method: 'POST'});
        });
    ''')  # JavaScript to notify server when tab closes
])

# Generate unique session ID
@app.callback(
    Output('session-id', 'data'),
    Input('interval', 'n_intervals'),
    State('session-id', 'data')
)
def initialize_session(n, session_id):
    if session_id is None:
        session_id = str(datetime.utcnow().timestamp())  # Unique session ID
        user_sessions[session_id] = {'start_time': datetime.utcnow()}
    return session_id

# Display time spent on the app
@app.callback(
    Output('timer-output', 'children'),
    Input('interval', 'n_intervals'),
    State('session-id', 'data')
)
def update_timer(n, session_id):
    if session_id in user_sessions:
        start_time = user_sessions[session_id]['start_time']
        elapsed = datetime.utcnow() - start_time
        return f"Time spent on app: {elapsed.seconds} seconds"
    return "Initializing session..."

# Handle app close event
@server.route('/close', methods=['POST'])
def app_closed():
    # Get session ID from request headers or other client-side data
    # For simplicity, this example assumes sessions are managed with dcc.Store
    for session_id, data in user_sessions.items():
        start_time = data['start_time']
        elapsed = datetime.utcnow() - start_time
        print(f"Session {session_id} closed. Time spent: {elapsed.seconds} seconds")
    return '', 200

if __name__ == '__main__':
    app.run_server(debug=True)
