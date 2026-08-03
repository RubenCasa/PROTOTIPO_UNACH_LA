with open('generar_informe_word.py', 'rb') as f:
    content = f.read()

content = content.replace(b'add_heading_apa(doc, "6.1 Variables acad', b'add_heading_apa(doc, "2.6.1 Variables acad')
content = content.replace(b'add_heading_apa(doc, "6.3 Viabilidad de implement', b'add_heading_apa(doc, "2.6.3 Viabilidad de implement')
content = content.replace(b'add_heading_apa(doc, "7.1 Seguridad de la inform', b'add_heading_apa(doc, "2.7.1 Seguridad de la inform')
content = content.replace(b'add_heading_apa(doc, "7.3 Aspectos legales y ', b'add_heading_apa(doc, "2.7.3 Aspectos legales y ')

content = content.replace(b'add_heading_apa(doc, "12.1 Referencias Bibliogr', b'add_heading_apa(doc, "8.1 Referencias Bibliogr')
content = content.replace(b'add_heading_apa(doc, "12.2 Documentaci', b'add_heading_apa(doc, "8.2 Documentaci')
content = content.replace(b'add_heading_apa(doc, "12.3 Normativa Consultada', b'add_heading_apa(doc, "8.3 Normativa Consultada')

with open('generar_informe_word.py', 'wb') as f:
    f.write(content)
