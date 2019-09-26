from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html", num = 3, color = "skyblue")
@app.route('/play/<num>')
def playNum(num):
    number = int(num)
    return render_template('index.html', num = number, color = "skyblue")
@app.route('/play/<num>/<color>')
def playNumcolor(num, color):
    number = int(num)
    coloring = color
    return render_template('index.html', num = number, color = coloring)
app.run(debug=True)