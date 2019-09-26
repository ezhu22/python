from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', row = 8, column = 8)
@app.route('/<column>')
def columns(column):
    col = int(column)
    return render_template('index.html', row = 8, column = col)
@app.route('/<row>/<column>')
def rowColumns(row, column):
    col = int(column)
    ro = int(row)
    return render_template('index.html', row = ro, column = col)

app.run(debug=True)