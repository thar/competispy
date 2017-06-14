from datetime import timedelta


class ConversorTiempos:
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

    # electronico: 19, 29
    conversionElectronico50 = timedelta(minutes=0, seconds=0, milliseconds=290).total_seconds()
    conversionElectronicoResto = timedelta(minutes=0, seconds=0, milliseconds=190).total_seconds()

    @staticmethod
    def obtener_modificacion_tiempo(entrada_base_datos):
        modificacion_tiempo = 0
        if entrada_base_datos['genero'] != 'FEMENINO' and entrada_base_datos['genero'] != 'MASCULINO':
            return modificacion_tiempo
        if entrada_base_datos['piscinaInscripcion'] == 25:
            modificacion_tiempo +=\
                ConversorTiempos.conversiones[entrada_base_datos['genero']][entrada_base_datos['estilo']][entrada_base_datos['distancia']]
        if entrada_base_datos['cronometrajeInscripcion'] == 'M':
            if entrada_base_datos['prueba'] != 50:
                modificacion_tiempo += ConversorTiempos.conversionElectronicoResto
            else:
                modificacion_tiempo += ConversorTiempos.conversionElectronico50
        return modificacion_tiempo

    @staticmethod
    def obtener_modificacion_tiempo_25(entrada_base_datos):
        modificacion_tiempo = 0
        if entrada_base_datos['genero'] != 'FEMENINO' and entrada_base_datos['genero'] != 'MASCULINO':
            return modificacion_tiempo
        if entrada_base_datos['piscinaInscripcion'] == 50:
            modificacion_tiempo +=\
                ConversorTiempos.conversiones[entrada_base_datos['genero']][entrada_base_datos['estilo']][entrada_base_datos['distancia']]
        if entrada_base_datos['cronometrajeInscripcion'] == 'M':
            if entrada_base_datos['prueba'] != 50:
                modificacion_tiempo += ConversorTiempos.conversionElectronicoResto
            else:
                modificacion_tiempo += ConversorTiempos.conversionElectronico50
        return modificacion_tiempo

    @staticmethod
    def convertir_a_tiempo_inscripcion(entrada_base_datos):
        entrada_base_datos['tiempoInscripcion'] -= ConversorTiempos.obtener_modificacion_tiempo(entrada_base_datos)

    @staticmethod
    def convertir_a_tiempo_database(entrada_base_datos):
        entrada_base_datos['tiempoInscripcion'] += ConversorTiempos.obtener_modificacion_tiempo(entrada_base_datos)

    @staticmethod
    def convertir_a_tiempo_inscripcion_25(entrada_base_datos):
        entrada_base_datos['tiempoInscripcion'] += ConversorTiempos.obtener_modificacion_tiempo_25(entrada_base_datos)

    @staticmethod
    def convertir_a_tiempo_database_25(entrada_base_datos):
        entrada_base_datos['tiempoInscripcion'] -= ConversorTiempos.obtener_modificacion_tiempo_25(entrada_base_datos)
