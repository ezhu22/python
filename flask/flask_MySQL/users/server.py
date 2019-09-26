from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
from datetime import datetime
app = Flask(__name__)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%b %d, %Y"):
    return value.strftime(format)

@app.template_filter('formatdatetimeupdate')
def format_datetimeupdate(value, format="%b %d, %Y at %I:%M %p"):
    return value.strftime(format)

@app.route('/')
def index():
    mysql = connectToMySQL('user')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template('index.html', all_users = users)

@app.route('/add_user')
def add_user():
    return render_template('create_user.html')

@app.route('/show/<num>')
def show_user(num):
    mysql = connectToMySQL('user')
    one_user = mysql.query_db("SELECT * FROM users WHERE user_id =" + num +";")
    print(one_user)
    return render_template('one_user.html', user_info = one_user[0])

@app.route('/edit/<num>')
def edit_user(num):
    mysql = connectToMySQL('user')
    this_user = mysql.query_db("SELECT * FROM users WHERE user_id =" + num +";")
    print(this_user)
    return render_template('update.html', user_info = this_user[0])

@app.route('/create_user', methods=['POST'])
def create_user():
    mysql = connectToMySQL('user')
    print(request.form)
    query = "INSERT INTO users (`first_name`, `last_name`, `email`, `created_at`, `updated_at`) VALUES (%(fn)s, %(ln)s, %(em)s, now(),  now());"
    data = {
        "fn": request.form['f_name'],
        "ln": request.form['l_name'],
        "em": request.form['email'],
    }
    new_user_id = mysql.query_db(query, data)
    return redirect('/')

@app.route('/update_user/<num>', methods=['POST'])
def update_user(num):
    mysql = connectToMySQL('user')
    print(request.form)
    query = "UPDATE users SET `first_name` = %(fn)s, `last_name` = %(ln)s, `email` = %(em)s, `updated_at` = now() WHERE (`user_id` = "+ num + ");"
    data ={
        "fn": request.form['f_name'],
        "ln": request.form['l_name'],
        "em": request.form['email'],
    }
    edit_user_id = mysql.query_db(query, data)
    return redirect('/')

@app.route('/delete_user/<num>')
def delete_user(num):
    mysql = connectToMySQL('user')
    delete_this_user = mysql.query_db("DELETE FROM users WHERE (`user_id` =" + num  +");")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)