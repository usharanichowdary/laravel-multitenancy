from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)

app.secret_key = 'webpage'

db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='flask_app'
)

@app.route('/')
def index():
    if 'username' in session:
        message = f"Welcome {session['username']}! You are logged in."
    else:
        message = 'Welcome to Flask MySQL app. Please log in or register.'
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        db.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials, please try again.'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
