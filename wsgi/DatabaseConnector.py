try:
    import os
    import pymongo
    import json

    test = False
    if not test:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        with open(current_directory + '/default_database_keys') as f:
            default_database_keys = json.loads(f.read())

        mongo_host = os.getenv('OPENSHIFT_MONGODB_DB_HOST', default_database_keys['MONGODB_DB_HOST'])
        mongo_port = os.getenv('OPENSHIFT_MONGODB_DB_PORT', default_database_keys['MONGODB_DB_PORT'])
        mongo_user = os.getenv('OPENSHIFT_MONGODB_DB_USERNAME', default_database_keys['MONGODB_DB_USERNAME'])
        mongo_pass = os.getenv('OPENSHIFT_MONGODB_DB_PASSWORD', default_database_keys['MONGODB_DB_PASSWORD'])

        client = pymongo.MongoClient(mongo_host + ':' + mongo_port)
        test = not client.db.authenticate(mongo_user, mongo_pass, source=default_database_keys['SOURCE'])

        db = client.competispy
        nadadores = db.nadadores
        relevos = db.relevos

except Exception, e:
    print 'test mode:', e
    test = True


class TestingDb():
    def insert(self, data):
        return
        print 'inserting:', data
        print '\n'

    def remove(self, key):
        pass

    def find_one(self, key):
        return None


def get_nadadores_db():
    if test:
        return TestingDb()
    else:
        return nadadores


def get_relevos_db():
    if test:
        return TestingDb()
    else:
        return relevos
