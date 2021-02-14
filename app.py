import flask
from flask import render_template, request, redirect, url_for, session
from events import Events_data
import requests
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        r = requests.get('http://localhost:5000/events')
        return render_template('index.html', events=json.loads(r.text))
    elif request.method == 'POST':
        event_id = request.form["event_id"]
        return redirect("/book/" + str(event_id))

@app.route('/book/<id>')
def book(id):
    r = requests.get('http://localhost:5000/events/{}'.format(id))
    return render_template('book.html', event=json.loads(r.text))

@app.route('/booking', methods=['POST'])
def booking():
    payload = {"event_id": request.form['event_id'], "name": request.form['name']}
    r = requests.post('http://localhost:5000/reservations', params=payload)
    res = json.loads(r.text)
    id = res['event_id']
    r2 = requests.get('http://localhost:5000/events/{}'.format(id))
    ev = json.loads(r2.text)
    data = {"reservation": res, "event": ev}
    return redirect(url_for('confirmation', data=json.dumps(data)))

@app.route('/confirmation')
def confirmation():
    data = request.args['data']
    return render_template('confirmation.html', data=json.loads(data))

if __name__ == "__main__":
    app.run(port=4000)
