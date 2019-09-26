from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "WHERE ARE YOU FROM?"
@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template("index.html")
@app.route('/result', methods =['POST'])
def result():
    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Please enter a name")
    if len(request.form['location']) < 1:
        is_valid = False
        flash("Please select your Dojo location.")
    if len(request.form['language']) < 1:
        is_valid = False
        flash("Please select your favorite language.")
    if not is_valid:
        return redirect('/')
    else:
        mysql = connectToMySQL('dojo_survey')
        print("Got Post Info")
        print(request.form)
        query = "INSERT INTO users (`name`, `location`, `language`, `comment`, `created_at`, `updated_at`) VALUES (%(nm)s, %(lt)s, %(ln)s, %(cm)s, now(),  now());"
        data ={
            "nm": request.form['name'],
            "lt": request.form['location'],
            "ln": request.form['language'],
            "cm": request.form['comment'],
        }
        insert_results = mysql.query_db(query, data)
        return render_template("/results.html", user_data = request.form)
if __name__ == "__main__":
    app.run(debug=True)