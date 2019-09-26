from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('c_r_pets')
    pets = mysql.query_db('SELECT * FROM pets;')
    print(pets)
    return render_template('index.html', all_pets = pets)

@app.route('/create_pet', methods=['POST'])
def add_pet_to_db():
    mysql = connectToMySQL('c_r_pets')
    print(request.form)
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(pn)s, %(pt)s, NOW(), NOW());"
    data = {
        "pn": request.form['p_name'],
        "pt": request.form['p_type']
    }
    new_pet_id = mysql.query_db(query, data)
    return redirect('/')
if __name__ =="__main__":
    app.run(debug=True)