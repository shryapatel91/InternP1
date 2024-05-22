from flask import Flask, redirect, url_for, session, request
import config
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)


app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

app.secret_key = 'your_secret_key'
# OAuth configuration
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='your_google_client_id',
    consumer_secret='your_google_client_secret',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Route for handling the login page
@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

# Callback route after successful authentication
@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    
    # Here you would typically save user_info data to your database and handle user authentication
    
    return 'Logged in as: ' + user_info.data['email']

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

# Index route
@app.route('/')
def index():
    return 'Welcome to the Backend Application!'

# Retrieve user's information
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)
