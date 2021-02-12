import flask
from flask_restful import Api, reqparse, abort, Resource
from events import Events_data

app = flask.Flask(__name__)
app.config["DEBUG"] = True
