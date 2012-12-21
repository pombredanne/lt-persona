LT-Persona
==========

Data repository and services for managing LT members and clients

Objectif
-------------
Gérer un référentiel des membres et clients LT 

Bootstrapper
-------------

Pour installer les packages nécessaire, il faut dans un virtualenv Python ou au sein de son système exécuter :
```
pip install -r requirements.pip
```

Ensuite pour lancer un serveur en local, il suffit de faire :
```
python lt_persona/main.py
```

Déployer
-------------

Il suffit d'installer les librairies nécessaires via les commandes ci-dessus, et de définir les variables d'environnements :
```
export PERSONA_DB_PATH=/opt/webapp/persona/clients.db
export LT_DOMAIN="lateral-thoughts.com"
export ADMIN_EMAIL=...
export ADMIN_PASSWORD=...
```

pour définir où la persistence sera effectuée.
