from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'signing your life away'

@app.template_filter('formatdatetime')
def format_datetime(value, format="%b %d, %Y"):
    return value.strftime(format)

@app.route('/')
def index():
    return render_template('index.html')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/enter_email', methods=['POST'])
def enter_email():
    print(request.form)
    # print("the email has been entered")
    is_valid = True
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter an email address.")
    if not is_valid:
        return redirect('/')
    else:
        if not EMAIL_REGEX.match(request.form['email']):
                flash("Email is invalid! Please try again.")
                return redirect('/')
        mysql = connectToMySQL('email_ver')
        # print(request.form)
        # print('the email has been confirmed')
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(em)s, now(), now());"
        data = {
            "em": request.form['email']
        }
        session['email'] = request.form['email']
        insert_new_email = mysql.query_db(query, data)
        return redirect('/success')

@app.route('/success')
def success():
    mysql = connectToMySQL('email_ver')
    query = "SELECT * FROM emails;"
    all_emails = mysql.query_db(query)
    flash("The email address you entered " + session['email']  + " is a valid email address! Thank you!")
    return render_template('success.html', all_emails = all_emails)


if __name__ == "__main__":
    app.run(debug=True)