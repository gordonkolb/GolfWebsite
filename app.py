from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
from mysql.connector import Error
from helpers import *
import json
import re



connection = create_connection("localhost", "root", "joepettit")
mycursor = connection.cursor()
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    #if 'loggedin' in session:
        #return redirect(url_for('homepage'))
    # Output message if something goes wrong...
    msg = ''
    #mycursor.execute("USE " + "pythonlogin" + ";")
    #mycursor.execute("SHOW COLUMNS FROM "+ "accounts" + ";")
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        mycursor.execute("USE pythonlogin;")
        mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = mycursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for("newUserHomepage", user=account[1]))
        else:
            # Account doesnt exist or username/password incorrect
            msg='Incorrect username/password!'
    return render_template('login.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('homepage'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        mycursor.execute("USE pythonlogin;")
        mycursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = mycursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            mycursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            connection.commit()
            msg = 'You have successfully registered!'

            mycursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = mycursor.fetchone()
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[2]

            return redirect(url_for("newUserHomepage", user=username))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/', methods=["POST", "GET"])
def homepage():
    # Check if user is loggedin
    if 'loggedin' in session:
        return redirect(url_for("newUserHomepage", user=session['username']))

    elif request.method == 'POST':
        if request.form.get("View Scores"):
            print("just if")
            return redirect(url_for("viewScores"))
        elif request.form.get("Enter New Score"):
            print("Elif")
            return redirect(url_for("enterNewScore"))
    return render_template("homepage.html")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/new/user/<user>', methods=["POST", "GET"])
def newUserHomepage(user):
    # Check if user is loggedin
    if 'loggedin' in session:
        if request.method == 'POST':
            if request.form.get("View Scores"):
                print("just if")
                return redirect(url_for("viewScores"))
            elif request.form.get("Enter New Score"):
                print("Elif")
                return redirect(url_for("enterNewScore"))
        return render_template("newUserHomepage.html", user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/New-Entry', methods=['GET', 'POST'])
def enterNewScore():
    data = ''
    if request.method == "POST":
        mycursor.execute("USE " + "foo" + ";")
        course = request.form['course']
        
        # search by course
        mycursor.execute("SELECT name, email from people WHERE name LIKE %s OR email LIKE %s", ("%" + course + "%", "%" + course + "%"))
        #conn.commit()
        data = mycursor.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and course == 'all': 
            mycursor.execute("SELECT name, email from people")
            #conn.commit()
            data = mycursor.fetchall()
        return render_template('enterscoresnew.html', data=data)
    return render_template('enterscoresnew.html', data=data)

@app.route('/courses.json', methods=['GET', 'POST'])
def senbackjson():
    mycursor.execute("USE " + "handicap" + ";")
    mycursor.execute("SELECT DISTINCT course from scores")
    data = mycursor.fetchall()
    courses = []
    for course in data:
        courses.append(course[0])

    courses_json = json.dumps(courses)
    return courses_json

@app.route('/View-Scores')
def viewScores():
    # Check if user is loggedin
    if 'loggedin' in session:
        columns = get_columns("handicap", "scores", mycursor)
        rows = get_rows("handicap", "scores", mycursor, session)
        return render_template("table.html", columns=columns, rows=rows)

'''
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html")
'''
'''
@app.route('/New-Entry')
def enterNewScore():
    return render_template("enterScores.html")
'''
if __name__ == "__main__":
   app.run(debug=True) #export FLASK_ENV=development, export FLASK_APP=app

