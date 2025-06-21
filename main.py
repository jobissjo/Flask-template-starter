from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

TEST_DB = 'test.db'

def init_db():
    with sqlite3.connect(TEST_DB) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
        conn.commit()

@app.route("/")
def main_page():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        with sqlite3.connect(TEST_DB) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            c.execute('SELECT * FROM user WHERE email=?', (email))
            user = c.fetchone()
        
        if not user:
            return redirect(url_for('login'))
        
        if  user.password != password:
            return redirect(url_for('login'))

        # if email and password are valid, redirect to home page
        return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register_fun():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            result = redirect(url_for('register_fun'))
            return result
        
        # check if email already exists
        with sqlite3.connect(TEST_DB) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM user WHERE email=?', (email,))
            user = c.fetchone()
        
        if user:
            return redirect(url_for('register_fun'))
        
        with sqlite3.connect(TEST_DB) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, password))
            conn.commit()

        # if success, redirect to login page, for login
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0')

