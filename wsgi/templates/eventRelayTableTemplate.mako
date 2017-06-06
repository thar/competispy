## -*- coding: utf-8 -*-
<%!
    from ConversorTiempos import ConversorTiempos
%>
<%namespace name="time_renderer" file="timeRendererTemplate.mako"/>
      <thead>
       <tr>
          <th data-priority="3">Posicion</th>
          <th>Club</th>
          <th data-priority="1">Tiempo</th>
          <th data-priority="1">Piscina</th>
          <th data-priority="4">Fecha</th>
          <th data-priority="6">Categoria</th>
          <th data-priority="5">Puntos</th>
       </tr>
      </thead>
      <tbody>
      % for relevo in relevos:
          <%
              ConversorTiempos.convertir_a_tiempo_inscripcion_25(relevo)
              if relevo['fechaInscripcion']:
                  try:
                      relevo['fechaInscripcion'] = relevo['fechaInscripcion'].strftime('%d-%m-%Y')
                  except Exception, e:
                      pass
              else:
                  relevo['fechaInscripcion'] = ''
          %>
          <tr ${'class="cnalcobendas"' if "ALCOBENDAS" in relevo['club'] else ''}>
              <td>${loop.index + 1}</td>
              <td>${relevo['club']}</td>
              <td>${time_renderer.format_delta_time(relevo['tiempoInscripcion'])}</td>
              <td>${relevo['piscinaInscripcion']}-${relevo['cronometrajeInscripcion']}</td>
              <td>${relevo['fechaInscripcion']}</td>
              <td>${relevo['categoria']}</td>
              <td>${puntos[loop.index] * 2}</td>
          </tr>
      % endfor
      </tbody>