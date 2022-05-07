from flask import Flask, render_template,jsonify,request
from psycopg2 import connect
from secretinfo import database, ip, port, username, password

con = connect(host=ip, port=port, database=database, user=username, password=password)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', firstname = "Scoring", lastname = "Team")

@app.route('/backend/')
def backend():
    return render_template('backend/index.html', firstname = "Scoring", lastname = "Team")

@app.route('/backend/event')
def event():
    return render_template('backend/event.html', firstname = "Scoring", lastname = "Team")

@app.route("/api/race", methods=["POST"])
def racedata():
    category = request.json['category']
    event = request.json['event']
    cur = con.cursor()
    if category == "":
        cur.execute('SELECT to_json(racer_info) FROM racer_info WHERE race_id =%s',(event,))
        data = cur.fetchall()
    else:
        if category == 'Choose Category':
            cur.execute('SELECT to_json(racer_info) FROM racer_info WHERE race_id =%s',(event,))
            data = cur.fetchall()
        else:
            cur.execute('SELECT to_json(racer_info) FROM racer_info,racer_id WHERE racer_info.bib_id = racer_id.bib_id AND racer_info.race_id = racer_id.race_id AND racer_id.category_id =%s AND racer_id.race_id = %s',(category,event,))
            data = cur.fetchall()
    list = []
    for row in data:
        list.append(row[0])
    return jsonify(list)

@app.route("/api/event", methods=["POST"])
def eventdata():
    cur = con.cursor()
    cur.execute('SELECT to_json(race) FROM race')
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(row[0])
    return jsonify(list)

@app.route("/api/dropdown/category", methods=["POST"])
def dropdown():
    cur = con.cursor()
    cur.execute('SELECT to_json(row(category.category_id,category.category)) FROM category')
    data = cur.fetchall()
    list = []
    for row in data:
        list.append(row[0])
    return jsonify(list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500)
