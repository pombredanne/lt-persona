from flask import jsonify
import json
import os


DOMAIN = os.environ['LT_DOMAIN']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
MEMBERS_URI = 'http://data.%s/persons/members#%s'
NAMESPACE = "http://ns.lateral-thoughts.com/lt/0.1/"

REF_DATA_EXTRACTOR = {
    'app_id': lambda user: user.id.text,
    'first_name': lambda user: user.name.given_name,
    'last_name': lambda user: user.name.family_name,
    'username': lambda user: user.login.user_name,
    'is_admin': lambda user: user.login.admin,
    'email': lambda user: "%s@%s" % (user.login.user_name, DOMAIN)
}


def get_members_from_google():
    users = []
    import gdata.apps.client
    client = gdata.apps.client.AppsClient(domain=DOMAIN)
    client.ClientLogin(email=ADMIN_EMAIL,
                       password=ADMIN_PASSWORD,
                       source='apps')
    client.ssl = True
    for user in client.RetrieveAllUsers().entry:
        ddata = {
            'uri': MEMBERS_URI % (DOMAIN, user.login.user_name),
        }
        for key, extractor in REF_DATA_EXTRACTOR.items():
            ddata[key] = extractor(user)
        users += [ddata]
    return users


def format_members_to_rdf(members):
    from rdflib.graph import Graph
    from rdflib import Literal, Namespace, URIRef
    from rdflib import RDF

    g = Graph()
    g.bind("lt", NAMESPACE)
    LT = Namespace(NAMESPACE)

    # Add triples using store's add method.
    for user in members:
        person = URIRef(user.get('uri'))
        g.add((person, RDF.type, LT["Person"]))
        for key, extractor in REF_DATA_EXTRACTOR.items():
            g.add((person, LT[key], Literal(user.get(key))))
    return g
