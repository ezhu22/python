from flask import Flask, render_template, request, redirect
from datetime import datetime
app = Flask(__name__)  

def format_datetime(value, format="%A, %d %B %Y %I:%M %p"):
    if value is None:
        return ""
    return value.strftime(format)

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/checkout', methods=['POST'])         
def checkout():
    print(request.form)
    strawberry_from_form = request.form['strawberry']
    straw = int(strawberry_from_form)
    raspberry_from_form = request.form['raspberry']
    rasp = int(raspberry_from_form)
    apple_from_form = request.form['apple']
    apple = int(apple_from_form)
    blackberry_from_form = request.form['blackberry']
    black = int(blackberry_from_form)
    first_name_from_form = request.form['first_name']
    last_name_from_form = request.form['last_name']
    student_id_from_form = request.form['student_id']
    total_fruit = sum((straw, rasp, apple, black))
    dt=datetime.now()
    time = format_datetime(dt)
    return render_template("checkout.html", 
    strawberry_on_template = strawberry_from_form,
    raspberry_on_template = raspberry_from_form, 
    apple_on_template = apple_from_form,
    blackberry_on_template = blackberry_from_form,
    first_name_on_template = first_name_from_form,
    last_name_on_template = last_name_from_form,
    student_id_on_template = student_id_from_form,
    total_fruit_on_template = total_fruit,
    time_on_template = time
    )

@app.route('/fruits')         
def fruits():
    return render_template("fruits.html")

if __name__=="__main__":   
    app.run(debug=True)    