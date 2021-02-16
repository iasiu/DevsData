import flask
from flask import render_template, request, redirect, url_for, session
import requests
import json
from werkzeug.exceptions import HTTPException

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        r = requests.get('http://localhost:5000/events')

        if str(r.status_code) == "404":
            return render_template('error.html', msg=json.loads(r.text)['message'])

        return render_template('index.html', events=json.loads(r.text))
    elif request.method == 'POST':
        event_id = request.form["event_id"]
        return redirect("/book/" + str(event_id))

@app.route('/book/<id>')
def book(id):
    r = requests.get('http://localhost:5000/events/{}'.format(id))

    if str(r.status_code) == "404":
        return render_template('error.html', msg=json.loads(r.text)['message'])

    return render_template('book.html', event=json.loads(r.text))

@app.route('/booking', methods=['POST'])
def booking():
    payload = {"event_id": request.form['event_id'], "name": request.form['name']}
    r = requests.post('http://localhost:5000/reservations', params=payload)

    if str(r.status_code) == "404":
        return render_template('error.html', msg=json.loads(r.text)['message'])

    res = json.loads(r.text)
    id = res['event_id']
    r2 = requests.get('http://localhost:5000/events/{}'.format(id))

    if str(r2.status_code) == "404":
        return render_template('error.html', msg=json.loads(r.text)['message'])

    ev = json.loads(r2.text)
    data = {"reservation": res, "event": ev}
    return redirect(url_for('confirmation', data=json.dumps(data)))

@app.route('/confirmation')
def confirmation():
    data = request.args['data']
    return render_template('confirmation.html', data=json.loads(data))

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == 'GET':
        return render_template('manage_code.html')
    else:
        code = request.form['code']
        r = requests.get('http://localhost:5000/reservations/' + str(code))

        if str(r.status_code) == "404":
            return render_template('error.html', msg=json.loads(r.text)['message'])

        res = json.loads(r.text)
        r2 = requests.get('http://localhost:5000/events/' + str(res['event_id']))

        if str(r2.status_code) == "404":
            return render_template('error.html', msg=json.loads(r.text)['message'])

        ev = json.loads(r2.text)
        data = {"reservation": res, "event": ev}
        return render_template('manage.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    code = request.form['code']
    name = request.form['name']
    event_id = request.form['event_id']
    payload = {'event_id': event_id, 'name': name}
    r = requests.put('http://localhost:5000/reservations/' + str(code), params=payload)

    if str(r.status_code) == "404":
        return render_template('error.html', msg=json.loads(r.text)['message'])
    elif str(r.status_code) == "200":
        return render_template('success.html', msg=r.text[1:-2])
    else:
        return render_template('unknown_error.html')

@app.route('/delete', methods=['POST'])
def delete():
    code = request.form['code']
    r = requests.delete('http://localhost:5000/reservations/' + str(code))

    if str(r.status_code) == "404":
        return render_template('error.html', msg=json.loads(r.text)['message'])
    elif str(r.status_code) == "200":
        return render_template('success.html', msg=r.text[1:-2])
    else:
        return render_template('unknown_error.html')

@app.errorhandler(HTTPException)
def handle_exception(e):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=4000)
