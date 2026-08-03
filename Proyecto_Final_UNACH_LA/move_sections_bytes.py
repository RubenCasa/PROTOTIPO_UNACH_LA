with open('generar_informe_word.py', 'rb') as f:
    lines = f.readlines()

start_idx = 967
end_idx = 1039
insert_idx = 581  # line right before # CAPÍTULO 3: FASE 2

red_lines = lines[start_idx:end_idx]
rest_of_lines = lines[:start_idx] + lines[end_idx:]

new_red_lines = []
for line in red_lines:
    line = line.replace(b'CAP\xcdTULO 5:', b'SECCI\xd3N 2.5:')
    line = line.replace(b'CAP\xccTULO 5:', b'SECCI\xd3N 2.5:')
    line = line.replace(b'5. MODELADO DEL ECOSISTEMA DE DATOS', b'2.5 MODELADO DEL ECOSISTEMA DE DATOS')
    line = line.replace(b'5.1 Diagrama de arquitectura', b'2.5.1 Diagrama de arquitectura')
    line = line.replace(b'5.1.1 Arquitectura actual', b'2.5.1.1 Arquitectura actual')
    line = line.replace(b'5.1.2 Arquitectura propuesta', b'2.5.1.2 Arquitectura propuesta')
    line = line.replace(b'5.2 Diagrama de flujo de datos', b'2.5.2 Diagrama de flujo de datos')
    line = line.replace(b'5.3 Actores involucrados', b'2.5.3 Actores involucrados')

    line = line.replace(b'CAP\xcdTULO 6:', b'SECCI\xd3N 2.6:')
    line = line.replace(b'CAP\xccTULO 6:', b'SECCI\xd3N 2.6:')
    line = line.replace(b'6. AN\xc1LISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS', b'2.6 AN\xc1LISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS')
    line = line.replace(b'6.1 Variables acad\xe9micas relevantes', b'2.6.1 Variables acad\xe9micas relevantes')
    line = line.replace(b'6.2 Indicadores potenciales', b'2.6.2 Indicadores potenciales')
    line = line.replace(b'6.3 Viabilidad de implementaci\xf3n', b'2.6.3 Viabilidad de implementaci\xf3n')

    line = line.replace(b'CAP\xcdTULO 7:', b'SECCI\xd3N 2.7:')
    line = line.replace(b'CAP\xccTULO 7:', b'SECCI\xd3N 2.7:')
    line = line.replace(b'7. RIESGOS Y CONSIDERACIONES', b'2.7 RIESGOS Y CONSIDERACIONES')
    line = line.replace(b'7.1 Seguridad de la informaci\xf3n', b'2.7.1 Seguridad de la informaci\xf3n')
    line = line.replace(b'7.2 Calidad de datos', b'2.7.2 Calidad de datos')
    line = line.replace(b'7.3 Aspectos legales y \xe9ticos', b'2.7.3 Aspectos legales y \xe9ticos')
    
    # Also fallback replacements using '?' or raw strings if encoding is different
    line = line.replace(b'CAP\xc3\x8dTULO 5:', b'SECCI\xc3\x93N 2.5:')
    line = line.replace(b'CAP\xc3\x8dTULO 6:', b'SECCI\xc3\x93N 2.6:')
    line = line.replace(b'CAP\xc3\x8dTULO 7:', b'SECCI\xc3\x93N 2.7:')
    line = line.replace(b'6. AN\xc3\x81LISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS', b'2.6 AN\xc3\x81LISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS')
    
    new_red_lines.append(line)

new_lines = rest_of_lines[:insert_idx] + new_red_lines + rest_of_lines[insert_idx:]

content = b''.join(new_lines)

# Now fix the chapter numbering for the rest of the chapters
# 8 -> 5
content = content.replace(b'CAP\xcdTULO 8:', b'CAP\xcdTULO 5:')
content = content.replace(b'CAP\xc3\x8dTULO 8:', b'CAP\xc3\x8dTULO 5:')
content = content.replace(b'Cap\xedtulo 8:', b'Cap\xedtulo 5:')
content = content.replace(b'8. ARQUITECTURA T\xc9CNICA', b'5. ARQUITECTURA T\xc9CNICA')
content = content.replace(b'8. ARQUITECTURA T\xc3\x89CNICA', b'5. ARQUITECTURA T\xc3\x89CNICA')

# 9 -> 6 (Note that earlier script called it 13 for some reason? Wait, let's look at `patch_informe.py`)
# Ah, I see `CAPTULO 13: RESULTADOS CONSOLIDADOS`.
content = content.replace(b'CAP\xcdTULO 13: RESULTADOS', b'CAP\xcdTULO 6: RESULTADOS')
content = content.replace(b'CAP\xc3\x8dTULO 13: RESULTADOS', b'CAP\xc3\x8dTULO 6: RESULTADOS')
content = content.replace(b'CAP\xcdTULO 9: RESULTADOS', b'CAP\xcdTULO 6: RESULTADOS')
content = content.replace(b'CAP\xc3\x8dTULO 9: RESULTADOS', b'CAP\xc3\x8dTULO 6: RESULTADOS')
content = content.replace(b'9. RESULTADOS CONSOLIDADOS', b'6. RESULTADOS CONSOLIDADOS')
content = content.replace(b'13. RESULTADOS CONSOLIDADOS', b'6. RESULTADOS CONSOLIDADOS')
content = content.replace(b'9.1 Resultados', b'6.1 Resultados')
content = content.replace(b'13.1 Resultados', b'6.1 Resultados')

# 10 -> 7
content = content.replace(b'CAP\xcdTULO 10: CONCLUSIONES', b'CAP\xcdTULO 7: CONCLUSIONES')
content = content.replace(b'CAP\xc3\x8dTULO 10: CONCLUSIONES', b'CAP\xc3\x8dTULO 7: CONCLUSIONES')
content = content.replace(b'10. CONCLUSIONES Y RECOMENDACIONES', b'7. CONCLUSIONES Y RECOMENDACIONES')
content = content.replace(b'10.1 Conclusiones del Prototipo', b'7.1 Conclusiones del Prototipo')
content = content.replace(b'10.2 Recomendaciones del Prototipo', b'7.2 Recomendaciones del Prototipo')

# 10.3 -> 7.3
content = content.replace(b'CAP\xcdTULO 10.3:', b'SECCI\xd3N 7.3:')
content = content.replace(b'CAP\xc3\x8dTULO 10.3:', b'SECCI\xc3\x93N 7.3:')
content = content.replace(b'10.3 Conclusiones sobre el Ecosistema', b'7.3 Conclusiones sobre el Ecosistema')

# 11 -> 7.4
content = content.replace(b'CAP\xcdTULO 11:', b'SECCI\xd3N 7.4:')
content = content.replace(b'CAP\xc3\x8dTULO 11:', b'SECCI\xc3\x93N 7.4:')
content = content.replace(b'11. RECOMENDACIONES ESTRAT\xc9GICAS INSTITUCIONALES', b'7.4 RECOMENDACIONES ESTRAT\xc9GICAS INSTITUCIONALES')
content = content.replace(b'11. RECOMENDACIONES ESTRAT\xc3\x89GICAS INSTITUCIONALES', b'7.4 RECOMENDACIONES ESTRAT\xc3\x89GICAS INSTITUCIONALES')
content = content.replace(b'11.1 Mejoras tecnol\xf3gicas', b'7.4.1 Mejoras tecnol\xf3gicas')
content = content.replace(b'11.1 Mejoras tecnol\xc3\xb3gicas', b'7.4.1 Mejoras tecnol\xc3\xb3gicas')
content = content.replace(b'11.2 Integraci\xf3n de plataformas', b'7.4.2 Integraci\xf3n de plataformas')
content = content.replace(b'11.2 Integraci\xc3\xb3n de plataformas', b'7.4.2 Integraci\xc3\xb3n de plataformas')
content = content.replace(b'11.3 Implementaci\xf3n de anal\xedtica de aprendizaje', b'7.4.3 Implementaci\xf3n de anal\xedtica de aprendizaje')
content = content.replace(b'11.3 Implementaci\xc3\xb3n de anal\xc3\xadtica de aprendizaje', b'7.4.3 Implementaci\xc3\xb3n de anal\xc3\xadtica de aprendizaje')
content = content.replace(b'11.4 Estrategias de gobernanza de datos', b'7.4.4 Estrategias de gobernanza de datos')

# 12 -> 8
content = content.replace(b'CAP\xcdTULO 12: BIBLIOGRAF', b'CAP\xcdTULO 8: BIBLIOGRAF')
content = content.replace(b'CAP\xc3\x8dTULO 12: BIBLIOGRAF', b'CAP\xc3\x8dTULO 8: BIBLIOGRAF')
content = content.replace(b'12. BIBLIOGRAF\xcdA Y REFERENCIAS', b'8. BIBLIOGRAF\xcdA Y REFERENCIAS')
content = content.replace(b'12. BIBLIOGRAF\xc3\x8dA Y REFERENCIAS', b'8. BIBLIOGRAF\xc3\x8dA Y REFERENCIAS')

# 13 -> 9 (Wait, earlier we saw chapter 13 was Resultados... let's check ANEXOS)
content = content.replace(b'CAP\xcdTULO 13: ANEXOS', b'CAP\xcdTULO 9: ANEXOS')
content = content.replace(b'CAP\xc3\x8dTULO 13: ANEXOS', b'CAP\xc3\x8dTULO 9: ANEXOS')
content = content.replace(b'13. ANEXOS', b'9. ANEXOS')

# Fix index
# Let's just find the FASE 1 block in the index and append the new sections
index_marker1 = b'"   2.4 Entregable 4'
new_index_lines = b'''
        "   2.5 Modelado del Ecosistema de Datos",
        "   2.6 An\xe1lisis de Oportunidades para Learning Analytics",
        "   2.7 Riesgos y Consideraciones",'''

with open('generar_informe_word.py', 'wb') as f:
    f.write(content)

print('Moved successfully.')
