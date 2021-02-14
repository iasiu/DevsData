import flask
from flask import render_template, request, redirect
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

@app.route('/book/<id>', methods=['POST', 'GET'])
def book(id):
    if request.method == 'GET':
        r = requests.get('http://localhost:5000/events/{}'.format(id))
        return render_template('book.html', event=json.loads(r.text))
    elif request.method == 'POST':
        payload = {'event_id': id, 'name': request.form['name']}
        requests.post('http://localhost:5000/reservations', params=payload)
        return redirect('/')


if __name__ == "__main__":
    app.run(port=4000)
