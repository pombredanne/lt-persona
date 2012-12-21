from flask import jsonify
import os

DOMAIN = os.environ['LT_DOMAIN']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']


def get_members_from_google():
    users = []
    import gdata.apps.client
    client = gdata.apps.client.AppsClient(domain=DOMAIN)
    client.ClientLogin(email=ADMIN_EMAIL,
                       password=ADMIN_PASSWORD,
                       source='apps')
    client.ssl = True
    for user in client.RetrieveAllUsers().entry:
        users += [{
            'app_id': user.id.text,
            'first_name': user.name.given_name,
            'last_name': user.name.family_name,
            'username': user.login.user_name,
            'is_admin': user.login.admin,
            'email': "%s@%s" % (user.login.user_name, DOMAIN),
        }]
    return jsonify(users)
