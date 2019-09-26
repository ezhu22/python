from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key ="login and registration is the key to your future"

@app.template_filter('formatdatetime')
def format_datetime(value, format="%b %d, %Y"):
    return value.strftime(format)

@app.route('/')
def index():
    return render_template('index.html')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
USER_INFO = []

@app.route("/email", methods=['POST'])
def email():
    #print(request.form['email'])
    found = False
    mysql = connectToMySQL('private_wall')        # connect to the database
    query = "SELECT users.email from users WHERE users.email = %(user)s;"
    data = { 'user': request.form['email'] }
    result = mysql.query_db(query, data)
    
    if result:
        found = True
    return render_template('partials/email.html', found=found)

@app.route("/usersearch", methods=['POST'])
def search():
    #print(request.form['email'])
    found = False
    mysql = connectToMySQL('private_wall')        # connect to the database
    query = "SELECT users.email from users WHERE users.email = %(user)s;"
    data = { 'user': request.form['search_email'] }
    result = mysql.query_db(query, data)
    
    if result:
        found = True
    return render_template('partials/search_friend.html', found=found)

@app.route('/check_requirements', methods=['POST'])
def check_requirements():
    is_valid = True
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter in your first name.")
    if not NAME_REGEX.match(request.form['first_name']):
        is_valid = False
        flash("Please make sure your first name only contains letters from the alphabet.")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please enter in your last name.")
    if not NAME_REGEX.match(request.form['last_name']):
        is_valid = False
        flash("Please make sure your last name only contains letters from the alphabet.")
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter in your email address.")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please make sure your email follows standard conventions, ie. 'blank@dojo.com'.")
    if len(request.form['password']) < 8 or len(request.form['password']) > 16:
        is_valid = False
        flash("Your password did not meet the character limit requirements.")
    space_check = re.search(r"\s", request.form['password'])
    if space_check != None:
        is_valid = False
        flash("Your password cannot contains a space.")
    capital_check = re.search(r"[A-Z]", request.form['password'])
    if capital_check == None:
        is_valid = False
        flash("Your password must contain at least 1 Upper-case letter.")
    lower_check = re.search(r"[a-z]", request.form['password'])
    if lower_check == None:
        is_valid = False
        flash("Your password must contain at least 1 lower-case letter.")
    num_check = re.search(r"[0-9]", request.form['password'])
    if num_check == None:
        is_valid = False
        flash("Your password must contain at least 1 number.")
    if len(request.form['confirm_password']) < 2:
        is_valid = False
        flash("Please confirm your password.")
    if not request.form['password'] == request.form['confirm_password']:
        is_valid = False
        flash("Your passwords do not match")
    if not is_valid:
        return redirect('/')
    else:
        global USER_INFO
        USER_INFO = request.form
        mysql = connectToMySQL('private_wall')
        query = "SELECT email FROM users WHERE email =\'" + request.form['email'] + "\';"
        check_email_repeat = mysql.query_db(query)
        if check_email_repeat == ():
            return redirect('/register_user')
        else:
            flash("This email is already in use. Please register another.")
            return redirect('/')

@app.route('/register_user')
def register_user():
    pw_hash = bcrypt.generate_password_hash(USER_INFO['password'])
    session['email'] = USER_INFO['email']
    session['register'] = 1
    mysql = connectToMySQL('private_wall')
    query = "INSERT INTO users (first_name, last_name, email, password_hash, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(ph)s, NOW(), NOW());"
    data = {
        "fn": USER_INFO['first_name'],
        "ln": USER_INFO['last_name'],
        "em": USER_INFO['email'],
        "ph": pw_hash
    }
    register_user_to_db = mysql.query_db(query, data)
    return redirect('/success')

@app.route('/success')
def success():
    global USER_INFO
    USER_INFO = []
    if 'email' not in session:
        flash("Something went wrong, please register here!")
        return redirect('/')
    else:
        mysql = connectToMySQL('private_wall')
        query = "SELECT id, first_name FROM users WHERE email =\'" + session['email'] + "\';"
        login_user = mysql.query_db(query)
        session['user_id'] = login_user[0]['id']
        if session['register'] == 1:
            flash("Thank you for registering! Welcome to the Club")
            session['register'] = 0
        return render_template('success.html', user = login_user[0])

@app.route('/login_user', methods=['POST'])
def login_user():
    is_valid = True
    if len(request.form['email']) < 2:
        is_valid = False
        flash("Please enter in your email address.")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please make sure your email follows standard conventions, ie. 'blank@dojo.com'.")
    if not is_valid:
        session.clear()
        return redirect ('/')
    else:
        session['register'] = 0
        mysql = connectToMySQL('private_wall')
        query = "SELECT id, email, password_hash FROM users WHERE email =\'" + request.form['email'] + "\';"
        login_user = mysql.query_db(query)
        if login_user == ():
            flash("Whoops, please try again.")
            return redirect('/')
        if bcrypt.check_password_hash(login_user[0]['password_hash'], request.form['password']):
            session['email'] = login_user[0]['email']
            session['user_id'] = login_user[0]['id']
            return redirect('/success')
        else: 
            flash("Whoops, please try again.")
            return redirect('/')

@app.route('/wall')
def display_wall():
    if 'user_id' not in session:
        flash("Something's not right.")
        session.clear()
        return redirect('/')
    user_id = session['user_id']
    mysql = connectToMySQL('private_wall')
    query = "SELECT id, email, first_name from users where id = %(num)s ;"
    data = {
        "num": user_id
    }
    check_user = mysql.query_db(query, data)
    print(check_user)
    if check_user == ():
        flash("Something's not right.")
        session.clear()
        return redirect('/')
    if check_user[0]['id'] == session['user_id'] and check_user[0]['email'] == session['email']:
        mysql = connectToMySQL('private_wall')
        query = ("SELECT first_name, last_name, id FROM users ORDER BY first_name;")
        collect_user_data = mysql.query_db(query)
        mysql = connectToMySQL('private_wall')
        query = ("SELECT users.first_name, messages.id, messages.content, messages.user_id, messages.post_to_user_id, messages.created_at FROM users LEFT JOIN messages ON users.id = messages.user_id ORDER BY created_at DESC")
        collect_all_message_data = mysql.query_db(query)
        return render_template('wall.html', logged_in_user = check_user[0], other_users = collect_user_data, all_messages = collect_all_message_data)
    else:
        flash("Something's not right.")
        session.clear()
        return redirect('/')

@app.route('/post_message/<from_user_id>/<to_user_id>', methods=['POST'])
def post_message(from_user_id, to_user_id):
    f_user_id = int(from_user_id)
    t_user_id = int(to_user_id)
    if not session['user_id'] == f_user_id:
        flash("You're not the expected user!")
        session.clear()
        return redirect('/')
    if len(request.form['message_box']) < 5:
        flash("Your message is too short! Minimum of 5 characters please!")
        return redirect('/wall')
    mysql = connectToMySQL('private_wall')
    query = ("INSERT INTO messages (content, created_at, updated_at, post_to_user_id, user_id) VALUES (%(ct)s , now(), now(), %(ti)s, %(ui)s);")
    data = {
        "ct": request.form['message_box'],
        "ui": f_user_id,
        "ti": t_user_id
    }
    insert_message_in_db = mysql.query_db(query, data)
    print(f_user_id)
    return redirect('/wall')

@app.route('/delete/<message_id>/<logged_in_user_id>')
def delete_post(message_id, logged_in_user_id):
    check_user_id = int(logged_in_user_id)
    if not session['user_id'] == check_user_id:
        flash("You can't do that!")
        session.clear()
        return redirect ('/')
    else:
        mysql = connectToMySQL('private_wall')
        query = ("DELETE FROM messages WHERE id = %(mi)s;")
        data = {
            "mi": message_id
        }
        delete_post = mysql.query_db(query, data)
        return redirect('/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)