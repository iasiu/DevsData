import flask
from flask_restful import Api, reqparse, abort, Resource
import random
import string

app = flask.Flask(__name__)
app.config["DEBUG"] = True #
api = Api(app)

DATA = {
    'events': [
        {'id': 0,
         'title': 'Jazz Concert',
         'start_date': '2021-02-14 18:00:00',
         'end_date': '2021-02-14 21:00:00',
         'thumbnail': 'https://media.resources.festicket.com/www/__sized__/photos/1_ZUTKNaz-thumbnail-800x460-90.jpg'
        },
        {'id': 1,
         'title': 'Rock Concert',
         'start_date': '2021-02-13 20:00:00',
         'end_date': '2021-02-13 23:00:00',
         'thumbnail': 'https://d6u22qyv3ngwz.cloudfront.net/ad/7d7W/great-clips-great-haircut-sale-rock-concert-small-5.jpg'
        },
        {'id': 2,
         'title': 'IT Days',
         'start_date': '2021-02-25 09:00:00',
         'end_date': '2021-02-28 18:00:00',
         'thumbnail': 'https://storage.googleapis.com/xmcom-wp-content-uploads/1/2018/1Blog-Thumbnail-341X271@2x-e1543274763520.jpg'
        },
        {'id': 3,
         'title': 'Icecream Workshop',
         'start_date': '2021-02-14 18:00:00',
         'end_date': '2021-02-14 21:00:00',
         'thumbnail': 'https://www.jealousgallery.com/Images/Prints/Dave-Buonaguidi-Have-A-Nice-Day-Ice-Cream-Cones.jpg?Action=thumbnail&Width=500'
        },

    ],

    'reservations': [
        {'event_id': 0,
         'name': 'Jan Lewandowski',
         'code': 'aaaa1111aaaa',
        },
        {'event_id': 0,
         'name': 'Ala Lewandowska',
         'code': 'bbbb1111aaaa',
        }
    ]
}

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('thumbnail')
parser.add_argument('event_id')
parser.add_argument('name')
parser.add_argument('code')

def abort_if_reservation_doesnt_exist(code):
    codes = []

    for r in DATA['reservations']:
        codes.append(r['code'])

    if code not in codes:
        abort(404, message="Reservation of code {} doesn't exist".format(code))

def abort_if_event_doesnt_exist(id):
    ids = []

    for e in DATA['events']:
        ids.append(e['id'])

    if int(id) not in ids:
        abort(404, message="Event of id {} doesn't exist".format(id))

def abort_if_event_does_exist(id):
    ids = []

    for e in DATA['events']:
        ids.append(e['id'])

    if int(id) in ids:
        abort(404, message="Event of id {} already exists".format(id))

def generate_reservation_code():
    length = 12
    chars = string.ascii_lowercase + string.ascii_uppercase + "0123456789"
    l_chars = list(chars)
    code = ""
    for i in range(length):
        code += random.choice(l_chars)
    return code

class Reservations(Resource):
    def get(self):
        return DATA['reservations']

    def post(self):
        args = parser.parse_args()

        code = generate_reservation_code()

        r = {'event_id': int(args['event_id']),
         'name': args['name'],
         'code': code,
        }

        DATA['reservations'].append(r)

        for r in DATA['reservations'][-10:]:
            if r['code'] == code:
                return r

class Reservation(Resource):
    def get(self, code):
        abort_if_reservation_doesnt_exist(code)
        for n, reservation in enumerate(DATA['reservations']):
            if reservation['code'] == code:
                return DATA['reservations'][n]

    def delete(self, code):
        abort_if_reservation_doesnt_exist(code)
        for n, reservation in enumerate(DATA['reservations']):
            if reservation['code'] == code:
                del DATA['reservations'][n]

        return '', 204

    def put(self, code):
        abort_if_reservation_doesnt_exist(code)

        args = parser.parse_args()

        r = {'event_id': int(args['event_id']),
         'name': args['name'],
         'code': code,
        }

        for n, reservation in enumerate(DATA['reservations']):
            if reservation['code'] == code:
                DATA['reservations'][n] = r

        return DATA['reservations'][n], 201


class Events(Resource):
    def get(self):
        return DATA['events']

    def post(self):
        args = parser.parse_args()

        e = {'id': int(DATA['events'][-1]['id']) + 1,
         'title': args['title'],
         'start_date': args['start_date'],
         'end_date': args['end_date'],
         'thumbnail': args['thumbnail'],
        }

        DATA['events'].append(e)

        return DATA['events'][-1]

class Event(Resource):
    def get(self, id):
        abort_if_event_doesnt_exist(id)
        for n, event in enumerate(DATA['events']):
            if int(event['id']) == int(id):
                return DATA['events'][n]

    def delete(self, id):
        abort_if_event_doesnt_exist(id)
        for n, event in enumerate(DATA['events']):
            if int(event['id']) == int(id):
                del DATA['events'][n]

        return '', 204

    def put(self, id):
        abort_if_event_doesnt_exist(id)

        args = parser.parse_args()

        e = {'id': int(id),
         'title': args['title'],
         'start_date': args['start_date'],
         'end_date': args['end_date'],
         'thumbnail': args['thumbnail'],
        }

        for n, event in enumerate(DATA['events']):
            if int(event['id']) == int(id):
                DATA['events'][n] = e

        return DATA['events'][n], 201

api.add_resource(Reservations, '/reservations')
api.add_resource(Reservation, '/reservations/<code>')
api.add_resource(Events, '/events')
api.add_resource(Event, '/events/<id>')

if __name__ == "__main__":
    app.run()
