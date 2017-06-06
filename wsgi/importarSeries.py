# -*- coding: UTF-8 -*-
import sys
import re
from datetime import datetime, timedelta
from pymongo import Connection

client = Connection()

cto_db = client.cto_esp_inv_mast_2017

nadadores = cto_db.nadadores
relevos = cto_db.relevos

nadadores_final = cto_db.nadadores_final
relevos_final = cto_db.relevos_final

relevos_final.remove({})
nadadores_final.remove({})

anoActual = 2017

eventoImportar = "cto. españa invierno master 2017".upper()
fechaImportar = datetime.strptime("02/02/2017", "%d/%m/%Y")

def getAnosCategoria(categoria):
    return [anoActual - categoria - i for i in range(5)]


#--------------------------------------------------------
test=False
testRelevos = False
if test:
    categoriaIn = sys.argv[2]
    pruebaIn = sys.argv[1].upper().split('-')
    anosCategoria = None
    
    try:
        pruebaIn[0]=int(pruebaIn[0])
        categoriaIn = int(categoriaIn)
        anosCategoria = getAnosCategoria(categoriaIn)
    except Exception, e:
        pruebaIn[0] = pruebaIn[0].lower()
        testRelevos = True
        #print 'prueba de relevos'
    
    if pruebaIn[1] == 'L':
       pruebaIn[1] = 'LIBRE'
    elif pruebaIn[1] == 'M':
       pruebaIn[1] = 'MARIPOSA'
    elif pruebaIn[1] == 'E':
       pruebaIn[1] = 'ESPALDA'
    elif pruebaIn[1] == 'B':
       pruebaIn[1] = 'BRAZA'
    elif pruebaIn[1] == 'S':
       pruebaIn[1] = 'ESTILOS'
    
    if pruebaIn[2] == 'M':
       pruebaIn[2] = 'MASCULINO'
    elif pruebaIn[2] == 'F':
       pruebaIn[2] = 'FEMENINO'
    elif pruebaIn[2] == 'X':
       pruebaIn[2] = 'MIXTO'
    
    print 'Prueba: ', pruebaIn, ' categoria: ', categoriaIn
#-------------------------------------------------------

#f = open('jornadas_ctoEspa.txt')
f = open('/home/qbo/Downloads/series_cto_inv_2017_palma')

jornada = None
#jornada = 0
datosFiltrados = []
serie = None
prueba = None
distancia = None
estilo = None
genero = None
isRelevo = False


conversiones = {}
conversiones['MASCULINO'] = {}
conversiones['FEMENINO'] = {}
conversiones['MIXTO'] = {}

conversiones['MASCULINO']['MARIPOSA'] = {}
conversiones['MASCULINO']['ESPALDA'] = {}
conversiones['MASCULINO']['BRAZA'] = {}
conversiones['MASCULINO']['LIBRE'] = {}
conversiones['MASCULINO']['ESTILOS'] = {}

conversiones['MASCULINO']['MARIPOSA'][50] = timedelta(minutes=0, seconds=0, milliseconds=300).total_seconds()
conversiones['MASCULINO']['MARIPOSA'][100] = timedelta(minutes=0, seconds=1, milliseconds=300).total_seconds()
conversiones['MASCULINO']['MARIPOSA'][200] = timedelta(minutes=0, seconds=3, milliseconds=100).total_seconds()
conversiones['MASCULINO']['ESPALDA'][50] = timedelta(minutes=0, seconds=1, milliseconds=100).total_seconds()
conversiones['MASCULINO']['ESPALDA'][100] = timedelta(minutes=0, seconds=2, milliseconds=500).total_seconds()
conversiones['MASCULINO']['ESPALDA'][200] = timedelta(minutes=0, seconds=5, milliseconds=700).total_seconds()
conversiones['MASCULINO']['BRAZA'][50] = timedelta(minutes=0, seconds=0, milliseconds=800).total_seconds()
conversiones['MASCULINO']['BRAZA'][100] = timedelta(minutes=0, seconds=2, milliseconds=300).total_seconds()
conversiones['MASCULINO']['BRAZA'][200] = timedelta(minutes=0, seconds=6, milliseconds=0).total_seconds()
conversiones['MASCULINO']['LIBRE'][50] = timedelta(minutes=0, seconds=0, milliseconds=700).total_seconds()
conversiones['MASCULINO']['LIBRE'][100] = timedelta(minutes=0, seconds=1, milliseconds=600).total_seconds()
conversiones['MASCULINO']['LIBRE'][200] = timedelta(minutes=0, seconds=3, milliseconds=400).total_seconds()
conversiones['MASCULINO']['LIBRE'][400] = timedelta(minutes=0, seconds=7, milliseconds=200).total_seconds()
conversiones['MASCULINO']['LIBRE'][800] = timedelta(minutes=0, seconds=15, milliseconds=700).total_seconds()
conversiones['MASCULINO']['LIBRE'][1500] = timedelta(minutes=0, seconds=29, milliseconds=500).total_seconds()
conversiones['MASCULINO']['LIBRE']['4x50'] = timedelta(minutes=0, seconds=2, milliseconds=800).total_seconds()
conversiones['MASCULINO']['ESTILOS'][100] = timedelta(minutes=0, seconds=0, milliseconds=0).total_seconds()
conversiones['MASCULINO']['ESTILOS'][200] = timedelta(minutes=0, seconds=4, milliseconds=900).total_seconds()
conversiones['MASCULINO']['ESTILOS'][400] = timedelta(minutes=0, seconds=10, milliseconds=0).total_seconds()
conversiones['MASCULINO']['ESTILOS']['4x50'] = timedelta(minutes=0, seconds=2, milliseconds=900).total_seconds()

conversiones['FEMENINO']['MARIPOSA'] = {}
conversiones['FEMENINO']['ESPALDA'] = {}
conversiones['FEMENINO']['BRAZA'] = {}
conversiones['FEMENINO']['LIBRE'] = {}
conversiones['FEMENINO']['ESTILOS'] = {}

conversiones['FEMENINO']['MARIPOSA'][50] = timedelta(minutes=0, seconds=0, milliseconds=300).total_seconds()
conversiones['FEMENINO']['MARIPOSA'][100] = timedelta(minutes=0, seconds=0, milliseconds=800).total_seconds()
conversiones['FEMENINO']['MARIPOSA'][200] = timedelta(minutes=0, seconds=2, milliseconds=400).total_seconds()
conversiones['FEMENINO']['ESPALDA'][50] = timedelta(minutes=0, seconds=1, milliseconds=0).total_seconds()
conversiones['FEMENINO']['ESPALDA'][100] = timedelta(minutes=0, seconds=2, milliseconds=200).total_seconds()
conversiones['FEMENINO']['ESPALDA'][200] = timedelta(minutes=0, seconds=5, milliseconds=700).total_seconds()
conversiones['FEMENINO']['BRAZA'][50] = timedelta(minutes=0, seconds=0, milliseconds=600).total_seconds()
conversiones['FEMENINO']['BRAZA'][100] = timedelta(minutes=0, seconds=2, milliseconds=0).total_seconds()
conversiones['FEMENINO']['BRAZA'][200] = timedelta(minutes=0, seconds=4, milliseconds=500).total_seconds()
conversiones['FEMENINO']['LIBRE'][50] = timedelta(minutes=0, seconds=0, milliseconds=400).total_seconds()
conversiones['FEMENINO']['LIBRE'][100] = timedelta(minutes=0, seconds=1, milliseconds=0).total_seconds()
conversiones['FEMENINO']['LIBRE'][200] = timedelta(minutes=0, seconds=2, milliseconds=400).total_seconds()
conversiones['FEMENINO']['LIBRE'][400] = timedelta(minutes=0, seconds=5, milliseconds=200).total_seconds()
conversiones['FEMENINO']['LIBRE'][800] = timedelta(minutes=0, seconds=11, milliseconds=900).total_seconds()
conversiones['FEMENINO']['LIBRE'][1500] = timedelta(minutes=0, seconds=22, milliseconds=300).total_seconds()
conversiones['FEMENINO']['LIBRE']['4x50'] = timedelta(minutes=0, seconds=1, milliseconds=600).total_seconds()
conversiones['FEMENINO']['ESTILOS'][100] = timedelta(minutes=0, seconds=0, milliseconds=0).total_seconds()
conversiones['FEMENINO']['ESTILOS'][200] = timedelta(minutes=0, seconds=3, milliseconds=100).total_seconds()
conversiones['FEMENINO']['ESTILOS'][400] = timedelta(minutes=0, seconds=7, milliseconds=500).total_seconds()
conversiones['FEMENINO']['ESTILOS']['4x50'] = timedelta(minutes=0, seconds=2, milliseconds=300).total_seconds()

conversiones['MIXTO']['LIBRE'] = {}
conversiones['MIXTO']['ESTILOS'] = {}

conversiones['MIXTO']['LIBRE'][400] = timedelta(minutes=0, seconds=7, milliseconds=200).total_seconds()
conversiones['MIXTO']['LIBRE'][800] = timedelta(minutes=0, seconds=15, milliseconds=700).total_seconds()
conversiones['MIXTO']['LIBRE'][1500] = timedelta(minutes=0, seconds=29, milliseconds=500).total_seconds()
conversiones['MIXTO']['ESTILOS'][400] = timedelta(minutes=0, seconds=10, milliseconds=0).total_seconds()
conversiones['MIXTO']['LIBRE']['4x50'] = timedelta(minutes=0, seconds=1, milliseconds=600).total_seconds()
conversiones['MIXTO']['ESTILOS']['4x50'] = timedelta(minutes=0, seconds=2, milliseconds=100).total_seconds()


#electronico: 19, 29
conversionElectronico50 = timedelta(minutes=0, seconds=0, milliseconds=290).total_seconds()
conversionElectronicoResto = timedelta(minutes=0, seconds=0, milliseconds=190).total_seconds()

re_nadadores = re.compile('\s+(?P<calle>\d+( [DI])?)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\d{4})\s+(?P<club>(\S+ )+)\s*(?P<marca>((\d{1,2}:)?\d{1,2}\.\d{1,2})|9:59:59.59)\s+(?P<piscina>\d{2}.*[ME])')
re_relevo = re_relevo = re.compile('\s+(?P<calle>\d+)\s+(?P<licencia>\S+)\s+(?P<nombre>(\S+ )+)\s*(?P<year>\+\d{2,3})\s*(?P<club>(\S+ )+)\s*(?P<marca>(\d{1,2}:)?\d{1,2}\.\d{1,2})\s+(?P<piscina>\d{2}.*[ME])')
re_serie = re.compile('\s*SERIE\s+(?P<serie>\d+)')
#re_serie = re.compile('\s*FINAL\s+(?P<serie>\d+)')
re_prueba = re.compile('\s*(?P<numero>\d+)\s+(?P<distancia>\S+)\s+m\.\s+(?P<estilo>\w+) (?P<genero>\w+)')
re_prueba_relevo = re.compile('\s*(?P<numero>\d+)\s+4x(?P<distancia>\S+)\s+(?P<estilo>\w+) (?P<genero>\w+)')
re_jornada = re.compile('\s*LISTAS DE SALIDA\s+(?P<jornada>\d+)\S\s+JORNADA')
#re_jornada = re.compile('(?P<jornada>\d+).{1,2}\s+jda.{1,2}(?P<sesion>\d+).{1,2}\s+sesi')


for l in f:
    l = l.decode('utf-8').encode('utf-8').rstrip()
    l = unicode(l, "utf-8")

    match_prueba = re_prueba.match(l)
    match_prueba_relevo = re_prueba_relevo.match(l)
    match_serie = re_serie.match(l)
    match_nadadores = re_nadadores.match(l)
    match_relevo = re_relevo.match(l)
    match_jornada = re_jornada.match(l)

    if match_serie:
        serie = int(match_serie.group('serie'))
    if match_jornada:
        jornada = int(match_jornada.group('jornada'))
    if match_prueba:
        prueba = int(match_prueba.group('numero'))
        distancia = match_prueba.group('distancia').strip()
        estilo = match_prueba.group('estilo').upper().strip()
        genero = match_prueba.group('genero').upper().strip()
        serie = None
        isRelevo = False
        distancia = int(distancia)
    if match_prueba_relevo:
        prueba = int(match_prueba_relevo.group('numero'))
        distancia = '4x' + match_prueba_relevo.group('distancia').strip()
        estilo = match_prueba_relevo.group('estilo').upper().strip()
        genero = match_prueba_relevo.group('genero').upper().strip()
        serie = None
        isRelevo = True

    if match_relevo and prueba and distancia and estilo and genero and serie and isRelevo:
        relevos_data = {}

        relevos_data['posicionInicial'] = 999
        relevos_data['jornada']=jornada
        relevos_data['prueba']=prueba
        relevos_data['distancia'] = distancia
        relevos_data['estilo'] = estilo
        relevos_data['genero'] = genero
        relevos_data['serie'] = serie
        relevos_data['calle'] = int(match_relevo.group('calle'))
        relevos_data['licencia'] = match_relevo.group('licencia').strip()
        relevos_data['club'] = match_relevo.group('club').upper().strip()
        relevos_data['nombre'] = match_relevo.group('nombre').strip()
        relevos_data['categoria'] = match_relevo.group('year').strip()
        tiempoInscripcion = match_relevo.group('marca').lstrip('0').lstrip(':').strip()
        separador = ','
        if '.' in tiempoInscripcion: separador = '.'
        if ':' in tiempoInscripcion:
            tiempoMinutos = int(tiempoInscripcion.split(':')[0])
            tiempoSegundos = int(tiempoInscripcion.split(':')[1].split(separador)[0])
            tiempoMilisegundos = int(tiempoInscripcion.split(':')[1].split(separador)[1])*10
        else:
            if separador in tiempoInscripcion:
                tiempoMinutos = 0
                tiempoSegundos = tiempoInscripcion.split(separador)[0]
                tiempoMilisegundos = tiempoInscripcion.split(separador)[1]
                if len(tiempoMilisegundos) == 3:
                    tiempoSegundos = tiempoSegundos + tiempoMilisegundos[0]
                    tiempoMilisegundos = tiempoMilisegundos[1:]
                tiempoSegundos = int(tiempoSegundos)
                tiempoMilisegundos = int(tiempoMilisegundos)*10
            else:
                tiempoMinutos = 0
                tiempoSegundos = int(tiempoInscripcion)/100
                tiempoMilisegundos = int(tiempoInscripcion)%100
        relevos_data['tiempoInscripcion'] = timedelta(minutes=tiempoMinutos, seconds=tiempoSegundos, milliseconds=tiempoMilisegundos).total_seconds()
        relevos_data['piscinaInscripcion'] = int(match_relevo.group('piscina')[0:2])
        relevos_data['cronometrajeInscripcion'] = match_relevo.group('piscina').strip()[-1].upper()
        relevos_data['fechaInscripcion'] = ''
        relevos_data['lugarInscripcion'] = ''

        relevo_pre = relevos.find_one({'distancia': relevos_data['distancia'], 'estilo': relevos_data['estilo'], 'genero': relevos_data['genero'], 'licencia': relevos_data['licencia']})
        if relevo_pre:
            #relevos_data['tiempoInscripcion'] = relevo_pre['tiempoInscripcion']
            relevos_data['fechaInscripcion'] = relevo_pre['fechaInscripcion']
            relevos_data['lugarInscripcion'] = relevo_pre['lugarInscripcion']
            relevos_data['posicionInicial'] = relevo_pre['posicionInicial']


        #print relevos_data
        if relevos_data['piscinaInscripcion'] == 50:
            relevos_data['tiempoInscripcion'] -= conversiones[relevos_data['genero']][relevos_data['estilo']][relevos_data['distancia']]
        if relevos_data['cronometrajeInscripcion'] == 'M':
            relevos_data['tiempoInscripcion'] += conversionElectronicoResto

        relevos_data['evento'] = eventoImportar.upper()
        relevos_data['fecha'] = fechaImportar

        #print relevos_data

        if not test:
            relevos_final.insert(relevos_data)
        if test and testRelevos and relevos_data['categoria'] == categoriaIn and relevos_data['distancia'] == pruebaIn[0] and relevos_data['estilo'] == pruebaIn[1] and relevos_data['genero'] == pruebaIn[2]:
            datosFiltrados.append(relevos_data)

    if match_nadadores and prueba and distancia and estilo and genero and serie and not isRelevo:
        swimmer_data = {}

        swimmer_data['jornada']=jornada
        swimmer_data['prueba']=prueba
        swimmer_data['distancia'] = distancia
        swimmer_data['estilo'] = estilo
        swimmer_data['genero'] = genero
        swimmer_data['serie'] = serie
        try:
            swimmer_data['calle'] = int(match_nadadores.group('calle'))
        except:
            swimmer_data['calle'] = int(match_nadadores.group('calle').split()[0])

        swimmer_data['posicionInicial'] = 999
        swimmer_data['licencia'] = match_nadadores.group('licencia').upper().strip()
        #if len(swimmer_data['licencia'])<9 and swimmer_data['licencia'][0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        #    swimmer_data['licencia'] = '0'*(9-len(swimmer_data['licencia'])) + swimmer_data['licencia']
        swimmer_data['nombre'] = match_nadadores.group('nombre').upper().strip()
        swimmer_data['nacimiento'] = int(match_nadadores.group('year'))
        swimmer_data['club'] = match_nadadores.group('club').upper().strip()
        tiempoInscripcion = match_nadadores.group('marca').upper().lstrip('0').lstrip(':').strip()
        separador = ','
        if '9:59:59.59' == tiempoInscripcion:
            tiempoMinutos = 59
            tiempoSegundos = 59
            tiempoMilisegundos = 59
        else:
            if '.' in tiempoInscripcion: separador = '.'
            if ':' in tiempoInscripcion:
                tiempoMinutos = int(tiempoInscripcion.split(':')[0])
                tiempoSegundos = int(tiempoInscripcion.split(':')[1].split(separador)[0])
                tiempoMilisegundos = int(tiempoInscripcion.split(':')[1].split(separador)[1])*10
            else:
                if separador in tiempoInscripcion:
                    tiempoMinutos = 0
                    tiempoSegundos = tiempoInscripcion.split(separador)[0]
                    tiempoMilisegundos = tiempoInscripcion.split(separador)[1]
                    if len(tiempoMilisegundos) == 3:
                        tiempoSegundos = tiempoSegundos + tiempoMilisegundos[0]
                        tiempoMilisegundos = tiempoMilisegundos[1:]
                    tiempoSegundos = int(tiempoSegundos)
                    tiempoMilisegundos = int(tiempoMilisegundos)*10
                else:
                    tiempoMinutos = 0
                    if len(tiempoInscripcion)<3:
                        tiempoSegundos = int(tiempoInscripcion)
                        tiempoMilisegundos = 0
                    else:
                        tiempoSegundos = int(tiempoInscripcion)/100
                        tiempoMilisegundos = int(tiempoInscripcion)%100
        swimmer_data['tiempoInscripcion'] = timedelta(minutes=tiempoMinutos, seconds=tiempoSegundos, milliseconds=tiempoMilisegundos).total_seconds()
        swimmer_data['piscinaInscripcion'] = int(match_nadadores.group('piscina')[0:2])
        swimmer_data['cronometrajeInscripcion'] = match_nadadores.group('piscina').strip()[-1].upper()
        swimmer_data['fechaInscripcion'] = ''
        swimmer_data['lugarInscripcion'] = ''

        swimmer_pre = nadadores.find_one({'distancia': swimmer_data['distancia'], 'estilo': swimmer_data['estilo'], 'genero': swimmer_data['genero'], 'licencia': swimmer_data['licencia']})
        if swimmer_pre:
            #swimmer_data['tiempoInscripcion'] = swimmer_pre['tiempoInscripcion']
            swimmer_data['fechaInscripcion'] = swimmer_pre['fechaInscripcion']
            swimmer_data['lugarInscripcion'] = swimmer_pre['lugarInscripcion']
            swimmer_data['posicionInicial'] = swimmer_pre['posicionInicial']


        #print swimmer_data
        if swimmer_data['piscinaInscripcion'] == 25:
            swimmer_data['tiempoInscripcion'] += conversiones[swimmer_data['genero']][swimmer_data['estilo']][swimmer_data['distancia']]
        if swimmer_data['cronometrajeInscripcion'] == 'M':
            if swimmer_data['prueba'] != 50:
                swimmer_data['tiempoInscripcion'] += conversionElectronicoResto
            else:
                swimmer_data['tiempoInscripcion'] += conversionElectronico50

        swimmer_data['evento'] = eventoImportar.upper()
        swimmer_data['fecha'] = fechaImportar

        #print swimmer_data

        if not test:
            nadadores_final.insert(swimmer_data)
        if test and not testRelevos and swimmer_data['nacimiento'] in anosCategoria and swimmer_data['distancia'] == pruebaIn[0] and swimmer_data['estilo'] == pruebaIn[1] and swimmer_data['genero'] == pruebaIn[2]:
            datosFiltrados.append(swimmer_data)

if test:
    datosFiltrados = sorted(datosFiltrados, key=lambda dato: dato['tiempoInscripcion'])
    for i in range(len(datosFiltrados)):
        if categoriaIn in datosFiltrados[i]:
            print "%d\t%d\t%s\t%s\t%dm-%s" % (i+1, datosFiltrados[i]['posicionInicial'], datosFiltrados[i]['club'], datosFiltrados[i]['tiempoInscripcion'], datosFiltrados[i]['piscinaInscripcion'], datosFiltrados[i]['cronometrajeInscripcion'])
        else:
            tiempo = datosFiltrados[i]['tiempoInscripcion']
            if datosFiltrados[i]['piscinaInscripcion'] == 25:
                tiempo -= conversiones[datosFiltrados[i]['genero']][datosFiltrados[i]['estilo']][datosFiltrados[i]['distancia']]
            if datosFiltrados[i]['cronometrajeInscripcion'] == 'M':
                if datosFiltrados[i]['prueba'] != 50:
                    tiempo -= conversionElectronicoResto
                else:
                    tiempo -= conversionElectronico50

            print "%d\t%d\t%s\t%s\t%s\t%dm-%s" % (i+1, datosFiltrados[i]['posicionInicial'], datosFiltrados[i]['nombre'], datosFiltrados[i]['club'], tiempo, datosFiltrados[i]['piscinaInscripcion'], datosFiltrados[i]['cronometrajeInscripcion'])

