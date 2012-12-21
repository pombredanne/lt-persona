from flask import request, jsonify
from flask import Response


class ClientHandler(object):

    def __init__(self, db):
        self.db = db

    def add(self):
        try:
            from main import Client
            client = Client(
                name=request.form['name'],
                address=request.form['address']
            )
            self.db.session.add(client)
            self.db.session.commit()
            return 201, client.id
        except Exception, e:
            return 400, "BAD REQUEST"

    def update(self):
        return 200

    def get(self, client_id):  # maps on GET /<id>
        from main import Client
        client = Client.query.get(client_id)
        if client:
            return 200, client
        else:
            return 404, "NOT FOUND"

    def list(self):
        import json
        from main import Client
        return 200, Client.query.all()

    def delete(self, client_id):
        from main import Client
        client = self.db.session.query(Client).get(client_id)
        if client:
            self.db.session.delete(client)
            self.db.session.commit()
        return 200, "DELETED"
