from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt 
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key ="I solemnly swear that I am up to no good."

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'(?!^[0-9]*$)^([a-zA-Z0-9]{4,16})$')
PASSWORD_REGEX = re.compile(r'(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9]{6,15})$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register_user', methods=['post'])
def register_user():
    if len(request.form['reg_first_name']) < 2 or len(request.form['reg_last_name']) < 2 or len(request.form['reg_username']) < 2 or len(request.form['reg_email']) < 2 or len(request.form['reg_password']) < 2 or len(request.form['reg_confirm_password']) < 2:
        flash("Please fill in all registration fields.")
        return redirect('/login')
    if not NAME_REGEX.match(request.form['reg_first_name']) or not NAME_REGEX.match(request.form['reg_last_name']):
        flash("Please do not include numbers in your name.")
        return redirect('/login')
    if not USERNAME_REGEX.match(request.form['reg_username']):
        flash("Your username does not meet the requirements.")
        return redirect('/login')
    if not EMAIL_REGEX.match(request.form['reg_email']):
        flash("Your email does not meet the requirements.")
        return redirect('/login')
    if not PASSWORD_REGEX.match(request.form['reg_password']):
        flash("Your password does not meet the requirements.")
        return redirect('/login')
    if not request.form['reg_password'] == request.form['reg_confirm_password']:
        flash("Your passwords do not match.")
        return redirect('/login')
    session['email'] = request.form['reg_email']
    pw_hash = pw_hash = bcrypt.generate_password_hash(request.form['reg_password'])
    mysql = connectToMySQL('login_registration_template')
    query = "INSERT INTO users (first_name, last_name, username, email, pw_hash, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(un)s, %(em)s, %(pwh)s, now(), now());"
    data = {
        "fn": request.form['reg_first_name'],
        "ln": request.form['reg_last_name'],
        "un": request.form['reg_username'],
        "em": session['email'],
        "pwh": pw_hash
    }
    register_user_to_db = mysql.query_db(query, data)
    mysql = connectToMySQL('login_registration_template')
    query = ('SELECT id from users where email = ''%(email)s'';')
    data = {
        "email": session['email']
    }
    user_id = mysql.query_db(query, data)
    session['id'] = user_id[0]['id']
    return redirect('/success')

@app.route('/success')
def success():
    if 'id' not in session:
        session.clear()
        flash("WHO ARE YOU?")
        return redirect('/login')
    else:
        mysql = connectToMySQL('login_registration_template')
        query = ("SELECT id, username, email FROM users WHERE id = %(id)s;")
        data = {
            "id": session['id']
        }
        check_user_info = mysql.query_db(query, data)
        if not check_user_info[0]['id'] == session['id'] and  not check_user_info[0]['email'] == session['email']:
            flash("Are you really " + check_user_info[0]['username'] + "?")
            session.clear()
            return redirect('/login')
        session['username'] = check_user_info[0]['username']
        return render_template('/success.html') 

@app.route('/login_user', methods=['POST'])
def login_user():
    mysql = connectToMySQL('login_registration_template')
    query = "SELECT id, email, pw_hash FROM users WHERE username = %(un)s;"
    data = {
        "un": request.form['login_username']
    }
    login_user = mysql.query_db(query, data)
    if login_user == ():
            flash("Whoops, there is nothing here!")
            return redirect('/login')
    if bcrypt.check_password_hash(login_user[0]['pw_hash'], request.form['login_password']):
        session['email'] = login_user[0]['email']
        session['id'] = login_user[0]['id']
        return redirect('/success')
    else: 
            flash("Whoops, please try again.")
            return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)