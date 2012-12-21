from flask import Flask, Response, Blueprint
from flask import request, render_template
from flask_rest import RESTResource
from clients import ClientHandler

app = Flask(__name__)

api = Blueprint("api", __name__, url_prefix="/api")

project_resource = RESTResource(
    name="client",  # name of the var to inject to the methods
    route="/clients",  # will be availble at /api/clients/*
    app=api,  # the app which should handle this
    actions=["add", "update", "delete", "get"],  # authorised actions
    handler=ClientHandler())  # the handler of the request

app.register_blueprint(api)


@app.route("/members")
def members():
    from members import get_members_from_google
    members = get_members_from_google()
    app.logger.error("Extracting members from google %s", members)
    return Response(str(members), mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
