## -*- coding: utf-8 -*-

<%!
    from datetime import timedelta

    def formatDeltaTime(tiempo):
        tiempo = timedelta(seconds=tiempo)
        segundos = tiempo.seconds
        microsegundos = tiempo.microseconds
        minutos = int(segundos/60)
        segundos -= minutos * 60
        decimas = microsegundos / 10000
        if minutos > 0:
            return "%d:%02d.%02d" % (minutos, segundos, decimas)
        else:
            return "%d.%02d" % (segundos, decimas)
%>

<%def name="format_delta_time(t)">${formatDeltaTime(t)}</%def>