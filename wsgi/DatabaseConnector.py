try:
    from pymongo import Connection

    client = Connection()

    cto_db = client.testing_db

    nadadores = cto_db.nadadores
    relevos = cto_db.relevos

    relevos.remove({})
    nadadores.remove({})
    test = False
except Exception:
    test = True


class TestingDb():
    def insert(self, data):
        print 'inserting:', data
        print '\n'


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
