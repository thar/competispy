## -*- coding: utf-8 -*-
<%!
    from ConversorTiempos import ConversorTiempos
%>
<%namespace name="time_renderer" file="timeRendererTemplate.mako"/>
      <thead>
      <tr>
          <th data-priority="5">Posicion</th>
          <th data-priority="5">Licencia</th>
          <th>Nombre</th>
          <th data-priority="6">Serie</th>
          <th data-priority="6">Calle</th>
          <th data-priority="5">Club</th>
          <th data-priority="1">Tiempo</th>
          <th data-priority="1">Piscina</th>
          <th data-priority="4">Fecha</th>
          <th data-priority="3">Nacimiento</th>
          <th data-priority="6">Puntos</th>
      </tr>
      </thead>
      <tbody>
      % for nadador in nadadores:
          <%
              ConversorTiempos.convertir_a_tiempo_inscripcion(nadador)
              if nadador['fechaInscripcion']:
                  try:
                      nadador['fechaInscripcion'] = nadador['fechaInscripcion'].strftime('%d-%m-%Y')
                  except Exception, e:
                      pass
              else:
                  nadador['fechaInscripcion'] = ''
              if not 'serie' in nadador:
                  nadador['serie'] = 0
              if not 'calle' in nadador:
                  nadador['calle'] = 0
          %>
          <tr ${'class="cnalcobendas"' if "ALCOBENDAS" in nadador['club'] else ''}>
              <td>${loop.index + 1}</td>
              <td>
              % if nadador['genero'] == 'FEMENINO' or nadador['genero'] == 'MASCULINO':
              <a href='http://rfen.es/publicacion/ranking/resultsBySwimmer.asp?l=${nadador['licencia']}&s=${nadador['genero'][0]}&m=mm&r=I' target='_blank'>
              ${nadador['licencia']}</a>
              % else:
              ${nadador['licencia']}
              % endif
              </td>
              <td>${nadador['nombre']}</td>
              <td>${nadador['serie']}</td>
              <td>${nadador['calle']}</td>
              <td>${nadador['club']}</td>
              <td>${time_renderer.format_delta_time(nadador['tiempoInscripcion'])}</td>
              <td>${nadador['piscinaInscripcion']}-${nadador['cronometrajeInscripcion']}</td>
              <td>${nadador['fechaInscripcion']}</td>
              <td>${nadador['nacimiento']}</td>
              <td>${puntos[loop.index]}</td>
          </tr>
      % endfor
      </tbody>