# -*- coding: UTF-8 -*-
import sys
sys.stdout = sys.stderr
import os
import re
import atexit
import cherrypy
from pymongo import MongoClient
import pymongo
from mako.lookup import TemplateLookup

current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory)

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

templates_lookup = TemplateLookup(directories=[current_directory + '/templates'], output_encoding='utf-8',
                                  encoding_errors='replace')

client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_HOST']+':'+os.environ['OPENSHIFT_MONGODB_DB_PORT'])
client.db.authenticate(os.environ['OPENSHIFT_MONGODB_DB_USERNAME'], os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'],
                       source='competispy')

db = client.competispy
nadadores = db.nadadores
relevos = db.relevos

anoActual = 2017

puntos = [0] * 16
for i in range(16):
    puntos[-1-i] = 1+i
puntos[0] = 19
puntos[1] = 16


def get_anos_categoria(categoria):
    return [anoActual - categoria - i for i in range(5)]


class Root(object):
    @cherrypy.expose
    def index(self):
        index_template = templates_lookup.get_template("indexTemplate.html")
        return index_template.render(anoActual=anoActual)

    @cherrypy.expose
    def search(self, distancia, estilo, genero, categoria, campeonato):
        if not 'x' in distancia:
            distancia = int(distancia)
            categoria = int(categoria)
            anosCategoria = get_anos_categoria(categoria)
            datos = nadadores.find(
                {'distancia': distancia, 'estilo': estilo, 'genero': genero, 'nacimiento': {'$in': anosCategoria},
                 'evento': {'$regex': campeonato, '$options': 'i'}}).sort(
                [("tiempoInscripcion", 1), ("serie", pymongo.DESCENDING), ("posicionInicial", 1)])
            index_template = templates_lookup.get_template("eventTableTemplate.mako")
            return index_template.render(nadadores=datos, puntos=puntos)
        else:
            if type(categoria) == int:
                categorias = [categoria, '+' + str(categoria)]
            elif categoria.startswith('+'):
                categorias = [int(categoria.strip('+')), categoria]
            else:
                categorias = [int(categoria), '+' + categoria]
            query = {'distancia': distancia, 'estilo': estilo, 'genero': genero, 'categoria': {'$in': categorias},
                     'evento': {'$regex': campeonato, '$options': 'i'}}
            datos = relevos.find(query).sort([("serie", pymongo.DESCENDING), ("tiempoInscripcion", 1),
                                              ("posicionInicial", 1)])
            return templates_lookup.get_template("eventRelayTableTemplate.mako").render(relevos=datos, puntos=puntos)

    @cherrypy.expose
    def searchNombre(self, nombre, campeonato):
        try:
            nombre = nombre.strip()
            if len(nombre) < 4:
                return ''
            datos = nadadores.find({'nombre': re.compile(nombre.upper()),
                                    'evento': {'$regex': campeonato, '$options': 'i'}})
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=datos)
        except Exception, e:
            print 'error: ', e
            return ""

    @cherrypy.expose
    def searchLicencia(self, licencia, campeonato):
        try:
            licencia = licencia.strip()
            if len(licencia) < 4:
                return ''
            datos = nadadores.find({'licencia': re.compile(licencia.upper()),
                                    'evento': {'$regex': campeonato, '$options': 'i'}})
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=datos)
        except Exception, e:
            print 'error: ', e
            return ""

    @cherrypy.expose
    def searchAvanzado(self, club, distancia, estilo, genero, anoInicial, anoFinal, campeonato):
        try:
            club = club.strip()
            if len(club) < 4:
                return ""
            elementosBusqueda = {}
            elementosBusqueda['evento'] = {'$regex': campeonato, '$options': 'i'}
            elementosBusqueda['club'] = re.compile(club.upper())
            if distancia != '0':
                elementosBusqueda['distancia'] = int(distancia)
            if estilo != '0':
                elementosBusqueda['estilo'] = estilo
            if genero != '0':
                elementosBusqueda['genero'] = genero
            if anoInicial != '0' or anoFinal != '0':
                elementosBusqueda['nacimiento'] = {}
            if anoInicial != '0':
                elementosBusqueda['nacimiento']["$gte"] = int(anoInicial)
            if anoFinal != '0':
                elementosBusqueda['nacimiento']["$lt"] = int(anoFinal)
        except Exception, e:
            print 'error: ', e
            return ""

        try:
            datos = nadadores.find(elementosBusqueda)
            return templates_lookup.get_template("swimmerTableTemplate.mako").render(nadadores=datos)
        except Exception, e:
            print 'error: ', e
            return ""

application = cherrypy.Application(Root(), script_name=None, config=None)

