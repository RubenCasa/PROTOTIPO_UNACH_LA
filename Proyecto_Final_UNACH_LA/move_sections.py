with open('generar_informe_word.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'CAPÍTULO 5: MODELADO DEL ECOSISTEMA' in line:
        start_idx = i - 1  # include the === header
    if 'CAPÍTULO 8: ARQUITECTURA TÉCNICA COMPLETA DEL SISTEMA' in line:
        end_idx = i - 1  # the === header of chapter 8

if start_idx == -1 or end_idx == -1:
    print('Failed to find indices', start_idx, end_idx)
    import sys
    sys.exit(1)

red_lines = lines[start_idx:end_idx]
rest_of_lines = lines[:start_idx] + lines[end_idx:]

# Find where to insert in Fase 1. Fase 2 starts at 'CAPÍTULO 3: FASE 2'
insert_idx = -1
for i, line in enumerate(rest_of_lines):
    if 'CAPÍTULO 3: FASE 2' in line:
        insert_idx = i - 1
        break

if insert_idx == -1:
    print('Failed to find insert index')
    import sys
    sys.exit(1)

# Modify the red lines to be 2.5, 2.6, 2.7
new_red_lines = []
for line in red_lines:
    line = line.replace('CAPÍTULO 5:', 'SECCIÓN 2.5:')
    line = line.replace('5. MODELADO DEL ECOSISTEMA DE DATOS', '2.5 MODELADO DEL ECOSISTEMA DE DATOS')
    line = line.replace('5.1 Diagrama de arquitectura', '2.5.1 Diagrama de arquitectura')
    line = line.replace('5.1.1 Arquitectura actual', '2.5.1.1 Arquitectura actual')
    line = line.replace('5.1.2 Arquitectura propuesta', '2.5.1.2 Arquitectura propuesta')
    line = line.replace('5.2 Diagrama de flujo de datos', '2.5.2 Diagrama de flujo de datos')
    line = line.replace('5.3 Actores involucrados', '2.5.3 Actores involucrados')

    line = line.replace('CAPÍTULO 6:', 'SECCIÓN 2.6:')
    line = line.replace('6. ANÁLISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS', '2.6 ANÁLISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS')
    line = line.replace('6.1 Variables académicas relevantes', '2.6.1 Variables académicas relevantes')
    line = line.replace('6.2 Indicadores potenciales', '2.6.2 Indicadores potenciales')
    line = line.replace('6.3 Viabilidad de implementación', '2.6.3 Viabilidad de implementación')

    line = line.replace('CAPÍTULO 7:', 'SECCIÓN 2.7:')
    line = line.replace('7. RIESGOS Y CONSIDERACIONES', '2.7 RIESGOS Y CONSIDERACIONES')
    line = line.replace('7.1 Seguridad de la información', '2.7.1 Seguridad de la información')
    line = line.replace('7.2 Calidad de datos', '2.7.2 Calidad de datos')
    line = line.replace('7.3 Aspectos legales y éticos', '2.7.3 Aspectos legales y éticos')
    new_red_lines.append(line)

new_lines = rest_of_lines[:insert_idx] + new_red_lines + rest_of_lines[insert_idx:]

content = ''.join(new_lines)
# Also we need to fix the numbering of the rest of the chapters.
# Currently they are 8, 9, 10, 11... they should go back to 5, 6, 7, 8, 9
content = content.replace('CAPÍTULO 8:', 'CAPÍTULO 5:')
content = content.replace('Capítulo 8:', 'Capítulo 5:')
content = content.replace('8. ARQUITECTURA TÉCNICA COMPLETA', '5. ARQUITECTURA TÉCNICA COMPLETA')

content = content.replace('CAPÍTULO 9:', 'CAPÍTULO 6:')
content = content.replace('Capítulo 9:', 'Capítulo 6:')
content = content.replace('9. RESULTADOS CONSOLIDADOS', '6. RESULTADOS CONSOLIDADOS')
content = content.replace('9.1 Resultados', '6.1 Resultados')

content = content.replace('CAPÍTULO 10:', 'CAPÍTULO 7:')
content = content.replace('Capítulo 10:', 'Capítulo 7:')
content = content.replace('10. CONCLUSIONES Y RECOMENDACIONES', '7. CONCLUSIONES Y RECOMENDACIONES')
content = content.replace('10.1 Conclusiones del Prototipo', '7.1 Conclusiones del Prototipo')
content = content.replace('10.2 Recomendaciones del Prototipo', '7.2 Recomendaciones del Prototipo')

content = content.replace('CAPÍTULO 10.3:', 'SECCIÓN 7.3:')
content = content.replace('10.3 Conclusiones sobre el Ecosistema Tecnológico', '7.3 Conclusiones sobre el Ecosistema Tecnológico')

content = content.replace('CAPÍTULO 11:', 'SECCIÓN 7.4:')
content = content.replace('Capítulo 11:', 'Sección 7.4:')
content = content.replace('11. RECOMENDACIONES ESTRATÉGICAS INSTITUCIONALES', '7.4 RECOMENDACIONES ESTRATÉGICAS INSTITUCIONALES')
content = content.replace('11.1 Mejoras tecnológicas', '7.4.1 Mejoras tecnológicas')
content = content.replace('11.2 Integración de plataformas', '7.4.2 Integración de plataformas')
content = content.replace('11.3 Implementación de analítica de aprendizaje', '7.4.3 Implementación de analítica de aprendizaje')
content = content.replace('11.4 Estrategias de gobernanza de datos', '7.4.4 Estrategias de gobernanza de datos')

content = content.replace('CAPÍTULO 12:', 'CAPÍTULO 8:')
content = content.replace('Capítulo 12:', 'Capítulo 8:')
content = content.replace('12. BIBLIOGRAFÍA Y REFERENCIAS', '8. BIBLIOGRAFÍA Y REFERENCIAS')

content = content.replace('CAPÍTULO 13:', 'CAPÍTULO 9:')
content = content.replace('Capítulo 13:', 'Capítulo 9:')
content = content.replace('13. ANEXOS', '9. ANEXOS')

# Fix index
index_marker = '"   2.4 Entregable 4: Documento de Lineamientos Éticos y de Gobernanza",'
new_index = index_marker + '''
        "   2.5 Modelado del Ecosistema de Datos",
        "   2.6 Análisis de Oportunidades para Learning Analytics",
        "   2.7 Riesgos y Consideraciones",'''
content = content.replace(index_marker, new_index)

with open('generar_informe_word.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Moved successfully.')
