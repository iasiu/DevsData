import flask
from flask import render_template
from events import Events_data
import requests
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    r = requests.get('http://localhost:5000/events')
    return render_template('index.html', events=json.loads(r.text))

@app.route('/book/<id>', methods=['POST', 'GET'])
def book(id):
    r = requests.get('http://localhost:5000/events/{}'.format(id))
    return r.text
    #return render_template('index.html', events=json.loads(r.text))


if __name__ == "__main__":
    app.run(port=4000)
