from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
# FOR ALTERING TABLE < YOU JUST NEED MANUAL MIGRATION SCRIPTS OR ANY MIGRATION TOOL(LIBRARY)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
TEST_DB = 'test.db'
def init_db():
    with sqlite3.connect(TEST_DB) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, password TEXT)')
        conn.commit()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(TEST_DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def main_page():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        cur = conn.execute('SELECT * FROM user WHERE email=?', (email,))
        user = cur.fetchone()

        if not user:
            flash('User not found')
            return redirect(url_for('login'))
        if  user['password'] != password:
            flash('Incorrect password')
            return redirect(url_for('login'))
        
        session['email'] = email

        # if email and password are valid, redirect to home page
        flash('Logged in successfully')
        return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_fun():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match')
            result = redirect(url_for('register_fun'))
            return result
        
        # check if email already exists
        db = get_db()
        cur = db.execute('SELECT * FROM user WHERE email=?', (email,))
        user = cur.fetchone() 
         
        
        if user:
            flash('User with this email already exists')
            return redirect(url_for('register_fun'))
        
        db.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, password))
        db.commit()

        # if success, redirect to login page, for login
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/about')
def about():
    email = session.get('email', None)
    if not email:
        flash('You must be logged in to access this page')
        return redirect(url_for('login'))
    return render_template('about.html')


@app.route('/contact')
def contact():
    email = session.get('email', None)
    if not email:
        flash('You must be logged in to access this page')
        return redirect(url_for('login'))
    return render_template('contact.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')

