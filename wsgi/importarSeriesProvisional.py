# -*- coding: UTF-8 -*-
import re
from datetime import datetime, timedelta
from ConversorTiempos import ConversorTiempos
from DatabaseConnector import get_nadadores_db, get_relevos_db

nadadores = get_nadadores_db()
relevos = get_relevos_db()

anoActual = 2017


def getAnosCategoria(categoria):
    return [anoActual - categoria - i for i in range(5)]


f = open('INSCRITOS_MASTER_VERANO_2017.txt')

evento = "XIII CTO. ANDALUCIA OPEN DE VERANO MASTER".upper()
fecha_evento = datetime.strptime("09/06/2017", "%d/%m/%Y")


class CompetitorParser(object):
    def __init__(self, regular_expression):
        self.regular_expression = re.compile(regular_expression)
        self.prueba_parser = None

    def specific_match(self, match_competitor):
        raise NotImplemented

    def match(self, line):
        match_competitor = self.regular_expression.match(line)
        if match_competitor and self.prueba_parser:
            competitor_data = {}
            competitor_data['posicionInicial'] = int(match_competitor.group('puesto'))
            competitor_data['serie'] = 0
            competitor_data['calle'] = 0
            competitor_data['jornada'] = 0
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

            competitor_data['evento'] = evento.upper()
            competitor_data['fecha'] = fecha_evento

            competitor_data.update(self.specific_match(match_competitor))
            self.prueba_parser.add_competitor_data(competitor_data)

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

    def specific_match(self, match_competitor):
        return {'nacimiento': int(match_competitor.group('year'))}


class RelevoParser(CompetitorParser):
    def __init__(self):
        super(RelevoParser, self).__init__(
            '\s*(?P<puesto>\d+)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\+\d{3})\s+(?P<club>(\S+ )+)\s*(?P<marca>(\d{1,2}:)?\d{1,2}\.\d{1,2})\s+(?P<piscina>\d{2}.{2}[ME])(\s+(?P<fecha>\d{2}/\d{2}/\d{4})\s+(?P<lugar>.*))?')

    def specific_match(self, match_competitor):
        return {'categoria': match_competitor.group('year').strip()}


class PruebaParser(object):
    def __init__(self, regular_expression):
        self.regular_expression = re.compile(regular_expression)
        self.prueba = None
        self.distancia = None
        self.estilo = None
        self.genero = None
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


class PruebaNadadores(PruebaParser):
    def __init__(self):
        super(PruebaNadadores, self).__init__(
            '\s*(?P<numero>\d+)\s+-\s+(?P<distancia>\S+)\s+m\.\s+(?P<estilo>\w+) (?P<genero>\w+)')

    def match(self, line):
        match_prueba = self.regular_expression.match(line)
        if match_prueba:
            print 'match prueba de nadadores!'
            self.prueba = int(match_prueba.group('numero'))
            self.distancia = int(match_prueba.group('distancia').strip())
            self.estilo = match_prueba.group('estilo').upper().strip()
            self.genero = match_prueba.group('genero').upper().strip()
            return True
        return False


class PruebaRelevos(PruebaParser):
    def __init__(self):
        super(PruebaRelevos, self).__init__(
            '\s*(?P<numero>\d+)\s+-\s+4x(?P<distancia>\S+)\s+(?P<estilo>\w+) (?P<genero>\w+)')

    def match(self, line):
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
parseadores_pruebas[0].set_db(nadadores)
parseadores_pruebas.append(PruebaRelevos())
parseadores_pruebas[1].add_competitor_parser(RelevoParser())
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
