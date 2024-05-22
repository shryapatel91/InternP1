from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import config
import pymysql
from authlib.integrations.flask_client import OAuth
import re

flag = 0
flag1 = 0
app = Flask(__name__)
app.secret_key = 'its_a_secret'
app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

def get_mysql_connection():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                 user=app.config['MYSQL_USER'],
                                 password=app.config['MYSQL_PASSWORD'],
                                 db=app.config['MYSQL_DB'],
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# OAuth Configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='575055763608-ipm8i4h7p9j548jcsilrbo3m91q14cvt.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

# Render login page
@app.route('/login')
def login():
    new_email = request.args.get('email')
    password = request.args.get('password')
    print('Inside login')
    session['new_email'] = new_email  # Store the new email in the session
    session['password'] = password
    print(session.get('new_email'))
    return google.authorize_redirect(redirect_uri=url_for('authorize', _external=True))

@app.route('/login/callback')
def authorize():
    global flag1
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    print('Inside authorize')
    print(user_info)
    print(session.get('new_email'))
    if flag1 == 0:
    # Check if the email matches the one from the registration form
        if 'email' in user_info and user_info['verified_email'] == True and user_info['email'] == session.get('new_email'):
            session['user_info'] = user_info
            return redirect(url_for('register', email=user_info['email'], password=session.get('password')))
        else:
            return 'Unauthorized Email Domain', 401
    else:
        if 'email' in user_info and user_info['verified_email'] == True:
            flag1 = 0
            connection = get_mysql_connection()
            cur = connection.cursor()
            session['user_info'] = user_info
            sql = "SELECT * FROM Authentication WHERE email=%s"
            cur.execute(sql, (user_info['email'],))
            user = cur.fetchone()
            if user:
                return redirect(url_for('dashboard'))
            else:
                sql = "INSERT INTO Authentication (email, password) VALUES (%s, %s)"
                password = user_info['email'].split('@')[0]
                cur.execute(sql, (user_info['email'], password))
                connection.commit()
                connection.close()
            return redirect(url_for('dashboard'))
        else:
            return 'Unauthorized Email Domain', 401


@app.route('/auth_try' , methods=['POST' , 'GET'])
def auth():
    global flag1
    flag1 = 1
    return google.authorize_redirect(redirect_uri=url_for('authorize', _external=True))

@app.route('/registration', methods=['POST'])
def check():
    email = request.form['email']
    password = request.form['password']
    return redirect(url_for('login', email=email, password=password))

# def validate_email(email):  
#     if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
#         return True  
#     return False

@app.route('/')
def main():
    global flag
    if flag == 0:
        session['login_attempts'] = 0
        session['login_blocked'] = False
        flag = 1
    return render_template('login.html')
@app.route('/login.html')
def log():
    global flag
    if flag == 0:
        session['login_attempts'] = 0
        session['login_blocked'] = False
        flag = 1
    return render_template('login.html')
@app.route('/register.html')
def reg():
    return render_template('register.html')
@app.route('/dashboard.html')
def dashboard():
    if 'user_info' not in session:
        return redirect(url_for('log'))
    return render_template('dashboard.html')
@app.route('/logout')
def logout():
    session.clear()  # Clear the user session

    # Check if session is cleared
    if 'user_info' in session:
        # Session is not cleared
        print("Session is not cleared. 'user_info' still exists in the session.")
    else:
        # Session is cleared
        print("Session is cleared. 'user_info' doesn't exist in the session.")

    return redirect('login.html')  # Redirect the user to the login page


@app.route('/loginForm', methods=['POST'])
def login_form():
    global flag
    #Initialize failed login attempts counter in session if not already present
    if 'login_attempts' not in session:
        session['login_attempts'] = 0
        session['login_blocked'] = False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_mysql_connection()
        cur = connection.cursor()

        # Check if email exists in Authentication table
        sql = "SELECT * FROM Authentication WHERE email=%s"
        cur.execute(sql, (email,))
        user = cur.fetchone()
        print(session['login_attempts'])
        print(session['login_blocked'])
        print(flag)
        if user:
            if user['Password'] == password:
                flag = 0
                session['login_attempts'] = 0  # Reset login attempts counter on successful login
                session['login_blocked'] = False
                session.pop('login_attempts', None)  # Reset login attempts counter on successful login
                return redirect(url_for('dashboard'))
            else:
                error = "Incorrect details"
                increment_login_attempts()  # Increment login attempts counter
        else:
            error = "Account doesn't exist"
            increment_login_attempts()
        
        connection.close()
        return redirect('login.html')
    

def increment_login_attempts():
    session['login_attempts'] += 1
    if session['login_attempts'] >= 3:  # If login attempts exceed 3
        session['login_blocked'] = True  # Set login blocked flag



# Route for registration page
@app.route('/registration', methods=['GET', 'POST'])
def register():
    print('Inside register')
    if 'user_info' not in session:
        print('User not verified')
        return redirect(url_for('login'))
    else:
        user_info = session.pop('user_info', None)  # Get verified user info and remove from session
        print( user_info)
        if user_info is None:
            return redirect(url_for('login'))
        
        email = request.args.get('email')
        print(user_info)
        password = request.args.get('password')
        connection = get_mysql_connection()
        cur = connection.cursor()

        try:
            # Check if email already exists
            sql = "SELECT * FROM Authentication WHERE email=%s"
            cur.execute(sql, (email,))
            existing_user = cur.fetchone()

            if existing_user:
                error = "User already exists"
                return redirect(url_for('main'), error=error)  # Assuming you handle the error in your main function
            # Insert new user into Authentication table
            sql = "INSERT INTO Authentication (email, password) VALUES (%s, %s)"
            cur.execute(sql, (email, password))
            connection.commit()
            return redirect(url_for('dashboard'))

        except Exception as e:
            app.logger.error('Error adding user to database: %s', str(e))
        finally:
            connection.close()

    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)
