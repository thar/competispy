# -*- coding: UTF-8 -*-
import re
from datetime import datetime, timedelta
from ConversorTiempos import ConversorTiempos
from DatabaseConnector import get_nadadores_db, get_relevos_db

nadadores = get_nadadores_db()
relevos = get_relevos_db()

'''
import requests
files = {'file': open('INSCRITOS_MASTER_VERANO_2017.pdf', 'rb')}
url = 'http://api2.pdfextractoronline.com:8089/tab2ex2/api'
payload = {'tab2exkey': 'XXXXXXXXXX', 'fileName': 'INSCRITOS_MASTER_VERANO_2017.pdf',
           'recognitionMethod': 'auto', 'outputFormat': 'TXT'}
r = requests.post(url, files=files, params=payload)
r.text.encode('utf-8')
'''

f = open('cto_madrid.txt')

evento = "XIII OPEN MASTER VERANO C.MADRID".upper()
fecha_evento = datetime.strptime("24/06/2017", "%d/%m/%Y")

nadadores.remove({'evento': evento})
relevos.remove({'evento': evento})


class CompetitorParser(object):
    def __init__(self, regular_expression):
        self.regular_expression = re.compile(regular_expression)
        self.prueba_parser = None

    def specific_match(self, match_competitor, competitor_data):
        raise NotImplemented

    def match(self, line):
        match_competitor = self.regular_expression.match(line)
        if match_competitor and self.prueba_parser:
            competitor_data = {}
            competitor_data['serie'] = self.prueba_parser.serie
            competitor_data['calle'] = 0
            competitor_data['jornada'] = self.prueba_parser.jornada
            competitor_data['prueba'] = self.prueba_parser.prueba
            competitor_data['distancia'] = self.prueba_parser.distancia
            competitor_data['estilo'] = self.prueba_parser.estilo
            competitor_data['genero'] = self.prueba_parser.genero
            competitor_data['licencia'] = match_competitor.group('licencia').strip()
            competitor_data['club'] = match_competitor.group('club').upper().strip()
            competitor_data['nombre'] = match_competitor.group('nombre').strip()
            tiempoInscripcion = match_competitor.group('marca').lstrip('0').lstrip(':').strip()
            competitor_data['tiempoInscripcion'] = CompetitorParser.parsear_tiempo_inscripcion(tiempoInscripcion)
            competitor_data['piscinaInscripcion'] = int(match_competitor.group('piscina')[0:2])
            competitor_data['cronometrajeInscripcion'] = match_competitor.group('piscina').strip()[-1].upper()
            ConversorTiempos.convertir_a_tiempo_database(competitor_data)

            competitor_data['evento'] = evento.upper()
            competitor_data['fecha'] = fecha_evento

            self.specific_match(match_competitor, competitor_data)
            self.prueba_parser.add_competitor_data(competitor_data)

    def update_inscription_time_data(self, competitor_data, match_competitor):
        competitor_data['posicionInicial'] = int(match_competitor.group('puesto'))
        fecha = match_competitor.group('fecha')
        if fecha:
            competitor_data['fechaInscripcion'] = fecha.strip()
        else:
            competitor_data['fechaInscripcion'] = ''
        lugar = match_competitor.group('lugar')
        if lugar:
            competitor_data['lugarInscripcion'] = lugar.strip()
        else:
            competitor_data['lugarInscripcion'] = ''

    def update_inscription_time_data_from_db(self, competitor_data, collection):
        competitor_pre = collection.find_one({'distancia': competitor_data['distancia'], 'estilo': competitor_data['estilo'], 'genero': competitor_data['genero'], 'licencia': competitor_data['licencia'], 'evento': competitor_data['evento']})
        if competitor_pre:
            competitor_data['fechaInscripcion'] = competitor_pre['fechaInscripcion']
            competitor_data['lugarInscripcion'] = competitor_pre['lugarInscripcion']
            competitor_data['posicionInicial'] = competitor_pre['posicionInicial']

    def set_prueba_parser(self, prueba_parser):
        self.prueba_parser = prueba_parser

    @staticmethod
    def parsear_tiempo_inscripcion(tiempo_inscripcion):
        separador = ','
        if '.' in tiempo_inscripcion:
            separador = '.'
        if ':' in tiempo_inscripcion:
            tiempoMinutos = int(tiempo_inscripcion.split(':')[0])
            tiempoSegundos = int(tiempo_inscripcion.split(':')[1].split(separador)[0])
            tiempoMilisegundos = int(tiempo_inscripcion.split(':')[1].split(separador)[1]) * 10
        else:
            if separador in tiempo_inscripcion:
                tiempoMinutos = 0
                tiempoSegundos = tiempo_inscripcion.split(separador)[0]
                tiempoMilisegundos = tiempo_inscripcion.split(separador)[1]
                if len(tiempoMilisegundos) == 3:
                    tiempoSegundos = tiempoSegundos + tiempoMilisegundos[0]
                    tiempoMilisegundos = tiempoMilisegundos[1:]
                tiempoSegundos = int(tiempoSegundos)
                tiempoMilisegundos = int(tiempoMilisegundos) * 10
            else:
                tiempoMinutos = 0
                tiempoSegundos = int(tiempo_inscripcion) / 100
                tiempoMilisegundos = int(tiempo_inscripcion) % 100
        return timedelta(minutes=tiempoMinutos, seconds=tiempoSegundos,
                         milliseconds=tiempoMilisegundos).total_seconds()


class NadadorParser(CompetitorParser):
    def __init__(self):
        super(NadadorParser, self).__init__(
            '\s*(?P<puesto>\d+)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\d{4})\s+(?P<club>(\S+ )+)\s*(?P<marca>\:?(\d{1,2}:)?\d{1,2}\.\d{1,2})\s+(?P<piscina>\d{2}.{2}[ME])(\s+(?P<fecha>\d{2}/\d{2}/\d{4})\s+(?P<lugar>.*))?')

    def specific_match(self, match_competitor, competitor_data):
        self.update_inscription_time_data(competitor_data, match_competitor)
        competitor_data['nacimiento'] = int(match_competitor.group('year'))


class RelevoParser(CompetitorParser):
    def __init__(self):
        super(RelevoParser, self).__init__(
            '\s*(?P<puesto>\d+)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\+\d{3})\s+(?P<club>(\S+ )+)\s*(?P<marca>(\d{1,2}:)?\d{1,2}\.\d{1,2})\s+(?P<piscina>\d{2}.{2}[ME])(\s+(?P<fecha>\d{2}/\d{2}/\d{4})\s+(?P<lugar>.*))?')

    def specific_match(self, match_competitor, competitor_data):
        self.update_inscription_time_data(competitor_data, match_competitor)
        competitor_data['categoria'] = match_competitor.group('year').strip()


class NadadorFinalParser(CompetitorParser):
    def __init__(self):
        super(NadadorFinalParser, self).__init__(
            '\s+(?P<calle>\d+( [DI])?)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\d{4})\s+(?P<club>(\S+ )+)\s*(?P<marca>((\d{1,2}:)?\d{1,2}\.\d{1,2})|9:59:59.59)\s+(?P<piscina>\d{2}.*[ME])$')

    def specific_match(self, match_competitor, competitor_data):
        self.update_inscription_time_data_from_db(competitor_data, nadadores)
        competitor_data['calle'] = int(match_competitor.group('calle'))
        competitor_data['nacimiento'] = int(match_competitor.group('year'))


class RelevoFinalParser(CompetitorParser):
    def __init__(self):
        super(RelevoFinalParser, self).__init__(
            '\s+(?P<calle>\d+)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\+\d{2,3})\s*(?P<club>(\S+ )+)\s*(?P<marca>(\d{1,2}:)?\d{1,2}\.\d{1,2})\s+(?P<piscina>\d{2}.*[ME])$')

    def specific_match(self, match_competitor, competitor_data):
        self.update_inscription_time_data_from_db(competitor_data, relevos)
        competitor_data['calle'] = int(match_competitor.group('calle'))
        competitor_data['categoria'] = match_competitor.group('year').strip()


class PruebaParser(object):
    def __init__(self):
        self.prueba = None
        self.distancia = None
        self.estilo = None
        self.genero = None
        self.serie = 0
        self.jornada = 0
        self.competitor_parsers = []
        self.competitors_data = []
        self.db = None

    def match(self, line):
        raise NotImplemented

    def add_competitor_parser(self, competitor_parser):
        competitor_parser.set_prueba_parser(self)
        self.competitor_parsers.append(competitor_parser)

    def add_competitor_data(self, competitor_data):
        self.competitors_data.append(competitor_data)

    def match_competitor(self, line):
        for competitor_parser in self.competitor_parsers:
            competitor_parser.match(line)

    def set_db(self, db):
        self.db = db

    def store(self):
        if self.db:
            for competitor in self.competitors_data:
                self.db.insert(competitor)


class PruebaConSerieParser(PruebaParser):
    def __init__(self):
        super(PruebaConSerieParser, self).__init__()
        self.serie_re = re.compile('\s*SERIE\s+(?P<serie>\d+)')

    def match(self, line):
        match_prueba_serie = self.serie_re.match(line)
        if match_prueba_serie:
            self.serie = int(match_prueba_serie.group('serie'))
            return False
        else:
            return self._match(line)

    def _match(self, line):
        raise NotImplemented



class PruebaNadadores(PruebaConSerieParser):
    def __init__(self):
        super(PruebaNadadores, self).__init__()
        self.regular_expression = re.compile(
            '\s*(?P<numero>\d+)\s+(-\s+)?(?P<distancia>\S+)\s+m\.\s+(?P<estilo>\w+) (?P<genero>\w+)')

    def _match(self, line):
        match_prueba = self.regular_expression.match(line)
        if match_prueba:
            print 'match prueba de nadadores!'
            self.prueba = int(match_prueba.group('numero'))
            self.distancia = int(match_prueba.group('distancia').strip())
            self.estilo = match_prueba.group('estilo').upper().strip()
            self.genero = match_prueba.group('genero').upper().strip()
            return True
        return False


class PruebaRelevos(PruebaConSerieParser):
    def __init__(self):
        super(PruebaRelevos, self).__init__()
        self.regular_expression = re.compile(
            '\s*(?P<numero>\d+)\s+((-\s)?)+4x(?P<distancia>\S+)\s+(?P<estilo>\w+) (?P<genero>\w+)')

    def _match(self, line):
        match_prueba_relevo = self.regular_expression.match(line)
        if match_prueba_relevo:
            print 'match prueba de relevos!'
            self.prueba = int(match_prueba_relevo.group('numero'))
            self.distancia = '4x' + match_prueba_relevo.group('distancia').strip()
            self.estilo = match_prueba_relevo.group('estilo').upper().strip()
            self.genero = match_prueba_relevo.group('genero').upper().strip()
            return True
        return False


parseadores_pruebas = []
parseadores_pruebas.append(PruebaNadadores())
parseadores_pruebas[0].add_competitor_parser(NadadorParser())
#parseadores_pruebas[0].add_competitor_parser(NadadorFinalParser())
parseadores_pruebas[0].set_db(nadadores)
parseadores_pruebas.append(PruebaRelevos())
parseadores_pruebas[1].add_competitor_parser(RelevoParser())
#parseadores_pruebas[1].add_competitor_parser(RelevoFinalParser())
parseadores_pruebas[1].set_db(relevos)

parseador_prueba_actual = None

for l in f:
    l = l.decode('utf-8').encode('utf-8').rstrip()
    l = unicode(l, "utf-8")

    for parserador_prueba in parseadores_pruebas:
        if parserador_prueba.match(l):
            parseador_prueba_actual = parserador_prueba

    if not parseador_prueba_actual:
        continue

    parseador_prueba_actual.match_competitor(l)

for parserador_prueba in parseadores_pruebas:
    parserador_prueba.store()
