# -*- coding: UTF-8 -*-
import sys
import traceback

sys.stdout = sys.stderr
import os
import re
import atexit
import cherrypy
import pymongo
from mako.lookup import TemplateLookup
import json
from bson.son import SON

current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory)

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

templates_lookup = TemplateLookup(directories=[current_directory + '/templates'], output_encoding='utf-8',
                                  encoding_errors='replace')

with open(current_directory + '/default_database_keys') as f:
    default_database_keys = json.loads(f.read())

mongo_host = os.getenv('OPENSHIFT_MONGODB_DB_HOST', default_database_keys['MONGODB_DB_HOST'])
mongo_port = os.getenv('OPENSHIFT_MONGODB_DB_PORT', default_database_keys['MONGODB_DB_PORT'])
mongo_user = os.getenv('OPENSHIFT_MONGODB_DB_USERNAME', default_database_keys['MONGODB_DB_USERNAME'])
mongo_pass = os.getenv('OPENSHIFT_MONGODB_DB_PASSWORD', default_database_keys['MONGODB_DB_PASSWORD'])

client = pymongo.MongoClient(mongo_host + ':' + mongo_port)
client.db.authenticate(mongo_user, mongo_pass, source=default_database_keys['SOURCE'])

db = client.competispy
individual_competitors = db.nadadores
relay_competitors = db.relevos

actual_year = 2017

points_per_position = [0] * 16
for i in range(16):
    points_per_position[-1 - i] = 1 + i
points_per_position[0] = 19
points_per_position[1] = 16


def get_years_in_category(category):
    return [actual_year - category - i for i in range(5)]


def print_exception(e):
    print 'error: ', e
    print '-' * 60
    traceback.print_exc(file=sys.stdout)
    print '-' * 60
    return ""


class Root(object):
    @cherrypy.expose
    def index(self):
        championships = individual_competitors.find().distinct("evento")
        pipeline = [
            {"$group": {"_id": {"evento": "$evento", "fecha": "$fecha"}}},
            {"$sort": SON([("_id.fecha", -1)])}
        ]
        pipeline_result = individual_competitors.aggregate(pipeline)
        if type(pipeline_result) == pymongo.command_cursor.CommandCursor:
            championships = [event['_id']['evento'] for event in list(pipeline_result)]
        else:
            championships = [event['_id']['evento'] for event in pipeline_result['result']]
        index_template = templates_lookup.get_template("indexTemplate.html")
        return index_template.render(anoActual=actual_year, championships=championships)

    @cherrypy.expose
    def search(self, distance, style, gender, category, championship):
        try:
            if not 'x' in distance:
                distance = int(distance)
                category = int(category)
                db_query_result = individual_competitors.find(
                    {'distancia': distance, 'estilo': style, 'genero': gender,
                     'nacimiento': {'$in': get_years_in_category(category)},
                     'evento': {'$regex': championship, '$options': 'i'}}).sort(
                    [("tiempoInscripcion", 1), ("serie", pymongo.DESCENDING), ("posicionInicial", 1)])
                return templates_lookup.get_template("eventTableTemplate.mako").render(nadadores=db_query_result,
                                                                                       puntos=points_per_position)
            else:
                if type(category) == int:
                    categories = [category, '+' + str(category)]
                elif category.startswith('+'):
                    categories = [int(category.strip('+')), category]
                else:
                    categories = [int(category), '+' + category]
                query = {'distancia': distance, 'estilo': style, 'genero': gender, 'categoria': {'$in': categories},
                         'evento': {'$regex': championship, '$options': 'i'}}
                db_query_result = relay_competitors.find(query).sort([("serie", pymongo.DESCENDING),
                                                                      ("tiempoInscripcion", 1), ("posicionInicial", 1)])
                return templates_lookup.get_template("eventRelayTableTemplate.mako").render(relevos=db_query_result,
                                                                                            puntos=points_per_position)
        except Exception, e:
            print_exception(e)
            return ""

    @cherrypy.expose
    def searchNombre(self, competitor_name, championship):
        try:
            competitor_name = competitor_name.strip()
            if len(competitor_name) < 4:
                return ''
            db_query_result = individual_competitors.find({'nombre': re.compile(competitor_name.upper()),
                                                           'evento': {'$regex': championship, '$options': 'i'}})
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=db_query_result)
        except Exception, e:
            print_exception(e)
            return ""

    @cherrypy.expose
    def searchLicencia(self, competitor_license_number, championship):
        try:
            competitor_license_number = competitor_license_number.strip()
            if len(competitor_license_number) < 4:
                return ''
            db_query_result = individual_competitors.find({'licencia': re.compile(competitor_license_number.upper()),
                                                           'evento': {'$regex': championship, '$options': 'i'}})
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=db_query_result)
        except Exception, e:
            print_exception(e)
            return ""

    @cherrypy.expose
    def searchAvanzado(self, club, distance, style, gender, start_born_year, end_born_year, championship):
        try:
            club = club.strip()
            if len(club) < 4:
                return ""
            search_query_filters = {'evento': {'$regex': championship, '$options': 'i'},
                                    'club': re.compile(club.upper())}
            if distance != '0':
                search_query_filters['distancia'] = int(distance)
            if style != '0':
                search_query_filters['estilo'] = style
            if gender != '0':
                search_query_filters['genero'] = gender
            if start_born_year != '0' or end_born_year != '0':
                search_query_filters['nacimiento'] = {}
            if start_born_year != '0':
                search_query_filters['nacimiento']["$gte"] = int(start_born_year)
            if end_born_year != '0':
                search_query_filters['nacimiento']["$lt"] = int(end_born_year)
        except Exception, e:
            print_exception(e)
            return ""

        try:
            db_query_result = individual_competitors.find(search_query_filters)
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=db_query_result)
        except Exception, e:
            print_exception(e)
            return ""

application = cherrypy.Application(Root(), script_name=None, config=None)

if __name__ == '__main__':
    cherrypy.quickstart(Root())
