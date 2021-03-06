from flask import Flask, Response, Blueprint
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, render_template
from flask_rest import RESTResource
from datetime import datetime

from clients import ClientHandler
from scheduler import start_scheduler

import os

app = Flask(__name__)

# set up database :
app.config['SQLALCHEMY_DATABASE_URI'] = os.\
    environ.get("PERSONA_DB_PATH",
                'sqlite:////tmp/test.db')

db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column('client_id', db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    address = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    _to_serialize = ("id", "name", "address", "created_at")

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.created_at = datetime.utcnow()

    def to_json(self):
        return {
            'name': self.name,
            'address': self.address,
            'created_at': str(self.created_at)}

db.create_all()

# set up api :
api = Blueprint("api", __name__, url_prefix="/api")

project_resource = RESTResource(
    name="client",  # name of the var to inject to the methods
    route="/clients",  # will be availble at /api/clients/*
    app=api,  # the app which should handle this
    actions=["add", "update", "delete", "get", "list"],  # authorised actions
    handler=ClientHandler(db))  # the handler of the request

app.register_blueprint(api)

start_scheduler()

@app.route("/members")
def members():
    from members import get_members_from_google, format_members_to_rdf
    import json
    mimetype = request.headers['Accept']
    members = get_members_from_google()
    if mimetype in ["application/n3", "application/turtle"]:
        _, format = mimetype.split("/")
        graph = format_members_to_rdf(members)
        return Response(graph.serialize(format=format), mimetype=mimetype)
    else:
        return Response(json.dumps(members), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
