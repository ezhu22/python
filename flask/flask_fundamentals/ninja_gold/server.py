from flask import Flask, render_template, request, redirect
import random

earned_gold = 0

app=Flask(__name__)
@app.route("/")
def ninja_gold():
    return render_template('index.html',score = earned_gold)

@app.route('/process_gold', methods=['POST'])
def process_gold():
    global earned_gold
    gamble = int((random.random()*10)+1)
    if request.form['whichbutton'] == 'farm':
        if gamble > 2:
            add_gold(int(random.random()*10)+10)
        else:
            sub_gold(int(random.random()*10)+10)
    if request.form['whichbutton'] == 'cave':
        if gamble > 3:
            add_gold(int(random.random()*5)+5)
        else:
            sub_gold(int(random.random()*5)+5)
    if request.form['whichbutton'] == 'house':
        if gamble > 4:
            add_gold(int(random.random()*50)+10)
        else:
            sub_gold(int(random.random()*50)+10)
    if request.form['whichbutton'] == 'casino':
        if gamble > 6:
            add_gold(int(random.random()*100)+20)
        else:
            sub_gold(int(random.random()*100)+20)
    if earned_gold < 0:
        earned_gold = 0
        return redirect('/game_over')
    else:
        return redirect('/')

def add_gold(gold):
    global earned_gold 
    earned_gold += gold

def sub_gold(gold):
    global earned_gold 
    earned_gold -= gold

@app.route('/game_over')
def game_over():
    return render_template('game_over.html')

if __name__ == "__main__":
    app.run(debug=True)
