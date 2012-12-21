

class ClientHandler(object):

    def add(self):
        return 201, 1

    def update(self):
        return 200

    def get(self, client_id):  # maps on GET /<id>
        return 200, "None"

    def delete(self, client):
        # do your stuff
        return 200, "DELETED"
