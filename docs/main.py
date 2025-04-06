from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Initialize Flask app
app = Flask(__name__)

# Secret key for sessions
app.secret_key = secrets.token_hex(16)

# Database connection
conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="your_host")
cur = conn.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)

        # Check if email already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_email = cur.fetchone()

        if existing_email:
            flash("Email is already in use")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address")
        elif not re.match(r'[A-Za-z]+', fullname):
            flash("Full name must contain letters and numbers")
        elif not password or not email:
            flash("Please fill out the form")
        else:
            cur.execute("INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)", (fullname, email, hashed_password))
            conn.commit()
            flash("You have registered successfully!")

    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form["email"]
        password = request.form["password"]

        # Check if user exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        if user:
            stored_password = user[3]
            if check_password_hash(stored_password, password):
                session['loggedin'] = True
                session['email'] = user[2]
                session['id'] = user[0]
                session['fullname'] = user[1]
                return redirect(url_for('home'))
            else:
                flash("Incorrect email/password")
        else:
            flash("User does not exist")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out. Would you like to regain access? Kindly log in.', category='error')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)