# -*- coding: utf-8 -*-
import os
import re

file_path = "generar_informe_word.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_sections = """
    # ========================================================================
    # CAPÍTULO 5: MODELADO DEL ECOSISTEMA DE DATOS
    # ========================================================================
    print("  >> Capítulo 5: Modelado del Ecosistema de Datos...")
    add_heading_apa(doc, "5. MODELADO DEL ECOSISTEMA DE DATOS", 1)

    add_heading_apa(doc, "5.1 Diagrama de arquitectura", 2)
    add_heading_apa(doc, "5.1.1 Arquitectura actual", 3)
    add_paragraph_apa(doc, "La infraestructura tecnológica actual de la UNACH se centraliza en el Data Center ubicado en el Campus Norte. Esta arquitectura cuenta con un \\"Backbone de Redes de Telecomunicaciones\\" impulsado por tecnología con inteligencia artificial (Juniper Mist) y mantiene respaldos inmutables en servidores locales y en la nube de CEDIA para asegurar la información crítica. Sin embargo, a nivel de software, los sistemas académicos como el SICOA y Moodle operan a menudo como \\"islas de digitalización\\" carentes de una articulación centralizada y automatizada.", indent=True, color=ROJO)
    
    add_heading_apa(doc, "5.1.2 Arquitectura propuesta", 3)
    add_paragraph_apa(doc, "La arquitectura propuesta se fundamenta en el proyecto institucional de Learning Analytics (Modelo UNACH-LA). Esta propuesta añade capas de integración donde la información extraída de los sistemas fuente pasa por un mecanismo estricto de anonimización (asignando identificadores únicos no reversibles). Posteriormente, los datos alimentan un motor analítico que centraliza la información para generar dashboards e indicadores clave de desempeño en tiempo real.", indent=True, color=ROJO)

    add_heading_apa(doc, "5.2 Diagrama de flujo de datos (DFD)", 2)
    add_paragraph_apa(doc, "Nivel 0 (Diagrama de contexto) Representa al Sistema Integrado de Analítica (UNACH-LA) como un proceso único central que interactúa con las entidades externas. Los estudiantes y docentes ingresan sus datos e interacciones, y el sistema devuelve tableros de control y resultados para la toma de decisiones.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Nivel 1 (Descomposición de procesos) Muestra el interior del sistema central dividiéndolo en sus subprocesos principales: Recolección, Anonimización, Procesamiento Analítico y Visualización de datos.", indent=True, color=ROJO)

    add_heading_apa(doc, "5.3 Actores involucrados", 2)
    add_paragraph_apa(doc, "Estudiantes: Son la población objetivo y fuente principal de datos. Proveen información demográfica, historial académico, calificaciones, asistencia y generan una huella digital constante mediante sus accesos y participación en los recursos del entorno Moodle. Son los beneficiarios finales de las estrategias de retención.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Docentes: Son usuarios clave tanto en la generación de datos (registrando calificaciones y asistencias en SICOA y evaluando tareas en Moodle) como en la utilización de la plataforma propuesta. El proyecto contempla la formación de docentes en analítica educativa para que puedan interpretar los dashboards y aplicar mejoras pedagógicas.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Coordinadores (y Autoridades): Incluye a directores de carrera, autoridades de facultad y autoridades institucionales. Su rol es estratégico, ya que consumen la información procesada por el modelo de analítica (tableros de control) para la gestión académica y la toma de decisiones basada en evidencia que reduzca la deserción estudiantil.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Administradores TIC: Involucra principalmente al personal de la Dirección de Tecnologías de la Información y Comunicación (DTIC) y la Coordinación de Desarrollo de Sistemas Informáticos (CODESI). Tienen el rol técnico vital de extraer los registros masivos de las plataformas, garantizar la infraestructura de servidores y redes, y aplicar los procesos de anonimización y asignación de identificadores únicos antes de entregar la información para el análisis.", indent=True, color=ROJO)
    doc.add_page_break()

    # ========================================================================
    # CAPÍTULO 6: ANÁLISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS
    # ========================================================================
    print("  >> Capítulo 6: Análisis de Oportunidades...")
    add_heading_apa(doc, "6. ANÁLISIS DE OPORTUNIDADES PARA LEARNING ANALYTICS", 1)
    add_paragraph_apa(doc, "El análisis de oportunidades se fundamenta en la ejecución del proyecto de investigación Modelo UNACH-LA, cuyo propósito es transformar los crecientes volúmenes de datos educativos en conocimiento accionable para mejorar los procesos académicos y reducir el riesgo de deserción en la Universidad Nacional de Chimborazo.", indent=True, color=ROJO)

    add_heading_apa(doc, "6.1 Variables académicas relevantes", 2)
    add_paragraph_apa(doc, "El modelo de Learning Analytics aprovecha datos provenientes de plataformas institucionales como SICOA y Moodle, los cuales se procesan bajo un estricto mecanismo de anonimización y seudonimización mediante un identificador único no reversible para proteger la identidad de los estudiantes.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Rendimiento: Se evalúa extrayendo datos históricos y actuales del SICOA, que incluyen las calificaciones obtenidas por asignatura (primer parcial, segundo parcial, recuperación y calificación final), puntajes de admisión, promedios de nivelación, asignaturas de la malla aprobadas y calificaciones de grado o titulación.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Participación: Se mide a través de la huella digital estudiantil capturada en el Learning Management System (Moodle), recopilando registros diarios de todas las acciones, recursos visualizados y eventos realizados en las aulas virtuales. Además, se complementa con el porcentaje de asistencia por asignatura y el registro de tutorías recibidas durante los periodos cursados.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Riesgo de deserción: Se monitorea mediante la identificación de patrones en datos críticos como el número de retiros y reingresos, asignaturas tomadas en segunda o tercera matrícula, y variables de contexto sociodemográfico que evidencien vulnerabilidad, tales como condiciones de salud, residencia (urbano/rural) y situación socioeconómica declarada.", indent=True, color=ROJO)

    add_heading_apa(doc, "6.2 Indicadores potenciales", 2)
    add_paragraph_apa(doc, "KPIs académicos: El proyecto busca consolidar la información en un prototipo funcional con tableros de control (dashboards) institucionales, los cuales mostrarán indicadores clave de desempeño (KPIs) para facilitar el seguimiento del progreso académico.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Alertas tempranas: Al integrar dimensiones pedagógicas y tecnológicas, los datos analizados permitirán generar alertas para proyectar análisis enfocados en disminuir el riesgo de deserción académica en grupos de estudio.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Predicción de desempeño: La analítica correlacional y longitudinal de los registros de SICOA (rendimiento) y Moodle (interacción) tiene el objetivo de traducir los datos masivos en conocimiento accionable, permitiendo proyectar escenarios para mejorar el rendimiento académico y guiar la toma de decisiones.", indent=True, color=ROJO)

    add_heading_apa(doc, "6.3 Viabilidad de implementación", 2)
    add_paragraph_apa(doc, "Técnica: La viabilidad técnica está respaldada por la reciente modernización del \\"Backbone de Redes de Telecomunicaciones\\" del campus, que incorporó tecnología de inteligencia artificial y amplió la cobertura, garantizando una alta disponibilidad y estabilidad para el procesamiento de datos. Asimismo, el uso de identificadores anonimizados viabiliza el cruce seguro de bases de datos masivas en formatos CSV y Excel. Sin embargo, existen limitaciones a superar, como la necesidad de actualizar librerías de software institucional para una mejor integración.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Operativa: A nivel operativo, el proyecto contempla la formación de al menos 50 docentes y gestores universitarios en analítica educativa, lo que garantizará que el personal sepa interpretar y utilizar los resultados del modelo. No obstante, el principal reto operativo radica en la demanda de tiempo para soporte técnico a usuarios finales y en la desvinculación de personal en el área de desarrollo de sistemas (CODESI), lo que limita la capacidad operativa para nuevos desarrollos de alto impacto.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Institucional: La implementación cuenta con la aprobación oficial de la Comisión de Investigación (Resolución No. 037-CIV-12-02-2026) y se alinea con la Política Pública para la Transformación Digital 2025-2030, que exige a las universidades la gestión basada en datos y el uso de tecnologías emergentes. Sin embargo, para garantizar su sostenibilidad, estudios de transformación digital en la UNACH recomiendan que estas iniciativas dejen de funcionar como \\"islas de digitalización\\" y se integren dentro de un plan institucional específico de transformación digital, requiriendo un fuerte compromiso de liderazgo y asignación de presupuesto.", indent=True, color=ROJO)
    doc.add_page_break()

    # ========================================================================
    # CAPÍTULO 7: RIESGOS Y CONSIDERACIONES
    # ========================================================================
    print("  >> Capítulo 7: Riesgos y Consideraciones...")
    add_heading_apa(doc, "7. RIESGOS Y CONSIDERACIONES", 1)
    
    add_heading_apa(doc, "7.1 Seguridad de la información", 2)
    add_paragraph_apa(doc, "La Universidad Nacional de Chimborazo (UNACH) rige la seguridad de su ecosistema tecnológico basándose en las \\"Políticas de Seguridad de la Información UNACH 2018\\", las cuales se alinean con estándares internacionales como ISO 27001 para mitigar riesgos y amenazas.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Protección de datos: Para evitar la pérdida de información crítica y garantizar su resguardo, la institución ha implementado copias de seguridad (backups) inmutables, alojadas tanto en servidores locales como en la nube de CEDIA. La normativa interna exige que las bases de datos, aplicativos y copias de seguridad se mantengan encriptadas. Además, los activos físicos del Data Center central están resguardados por sistemas de videovigilancia y acceso restringido.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Accesos: El ingreso a la infraestructura tecnológica y sistemas de información está estrictamente normado mediante un sistema de gestión de credenciales (roles y privilegios). Recientemente, se implementó un nuevo servidor Radius para fortalecer el control seguro de la autenticación de usuarios. Para los administradores que requieran conexiones desde el exterior, el acceso remoto a los servidores institucionales se realiza exclusivamente a través de Redes Privadas Virtuales (VPN) con encriptación.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Privacidad: La política institucional clasifica a los datos personales (como nombres, etnia, lugar de procedencia, estado de salud o vulnerabilidades económicas) estrictamente como información confidencial. Su uso está restringido al cumplimiento de actividades institucionales formales, quedando prohibida cualquier divulgación sin la debida autorización.", indent=True, color=ROJO)

    add_heading_apa(doc, "7.2 Calidad de datos", 2)
    add_paragraph_apa(doc, "Para asegurar que los modelos de Learning Analytics (como el proyecto UNACH-LA) ofrezcan predicciones y dashboards confiables, los datos deben cumplir tres características técnicas fundamentales:", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Integridad: Se garantiza que la información no ha sido modificada ni alterada sin autorización. Para lograrlo, los sistemas académicos (como SICOA) tienen habilitadas pistas de auditoría (logs) no editables que registran cada transacción, identificando al responsable de cualquier inserción, actualización o borrado de datos sensibles. Ningún usuario, ni siquiera los administradores o desarrolladores, puede modificar información directamente en la base de datos de producción sin seguir un estricto protocolo de control de cambios.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Consistencia: Dado que la infraestructura funciona en muchas ocasiones como \\"islas de digitalización\\", el proyecto UNACH-LA resuelve el cruce de información (entre SICOA y Moodle) mediante la creación de un identificador único no reversible. Esto asegura que los historiales académicos, de asistencia y de interacción digital coincidan exactamente para el mismo individuo, permitiendo efectuar análisis longitudinales y correlacionales sin inconsistencias en las bases de datos.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Disponibilidad: La disponibilidad permanente de la información se ha visto robustecida mediante el proyecto \\"Backbone de Redes de Telecomunicaciones\\", impulsado por tecnología de inteligencia artificial Juniper Mist. Esto permite alcanzar un índice de disponibilidad de red del 99%. A nivel de servidores, el Data Center institucional cuenta con estándares de redundancia diseñados para evitar interrupciones.", indent=True, color=ROJO)

    add_heading_apa(doc, "7.3 Aspectos legales y éticos", 2)
    add_paragraph_apa(doc, "La extracción de datos masivos para el seguimiento académico conlleva responsabilidades legales en el marco jurídico ecuatoriano y políticas internas.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Protección de datos personales: Todo el ecosistema opera bajo el cumplimiento de la Constitución de la República y la Ley Orgánica de Protección de Datos Personales, que exigen medidas de seguridad rigurosas frente a la información ciudadana. En estricto apego a esta ley, el requerimiento de datos para el modelo UNACH-LA establece como condición obligatoria la anonimización y/o seudonimización de toda la información entregada por Secretaría Académica y la Dirección de TICs (DTIC), garantizando la no identificación directa de los titulares de los datos.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Consentimiento: De acuerdo con el Art. 66 de la Constitución, el procesamiento o distribución de datos requiere la autorización de su titular o un mandato de la ley. Para fines del uso institucional, el personal y los proveedores firman acuerdos de confidencialidad y responsabilidades respecto al manejo de los activos. En el caso de la analítica de aprendizaje (UNACH-LA), al utilizar un mecanismo ciego de seudonimización (donde el dato personal se reemplaza por un código alfanumérico), se mitiga el riesgo de vulnerar la intimidad estudiantil, actuando bajo el amparo de la Resolución Oficial de la Comisión de Investigación de la UNACH (No. 037-CIV-12-02-2026).", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Uso responsable de información académica: El acceso a los datos extraídos tiene como única finalidad la investigación y el desarrollo de estrategias para la retención estudiantil. Existe un documento de compromiso firmado por los miembros del equipo de investigación (liderado por la Dirección del Proyecto UNACH-LA), en el cual se obligan a dar fiel cumplimiento a la normativa aplicable sobre el buen uso de los datos y a utilizarlos estrictamente con fines investigativos. Además, las políticas de la universidad prohíben categóricamente el uso de la infraestructura o bases de datos para suministrar información con el fin de obtener beneficios propios o de terceros.", indent=True, color=ROJO)
    doc.add_page_break()
"""

# Replace current chapter 5 header and content, renumber the rest.
# Find where Capítulo 5 starts:
cap5_marker = "    # ========================================================================\n    # CAPÍTULO 5:"
parts = content.split(cap5_marker)

if len(parts) == 2:
    part1, part2 = parts
    # Adjust part2 numbering
    part2 = part2.replace("CAPÍTULO 5:", "CAPÍTULO 8:")
    part2 = part2.replace("Capítulo 5:", "Capítulo 8:")
    part2 = part2.replace("5. ARQUITECTURA", "8. ARQUITECTURA")

    part2 = part2.replace("CAPÍTULO 6:", "CAPÍTULO 9:")
    part2 = part2.replace("Capítulo 6:", "Capítulo 9:")
    part2 = part2.replace("6. RESULTADOS", "9. RESULTADOS")
    part2 = part2.replace("6.1 Resultados", "9.1 Resultados")

    part2 = part2.replace("CAPÍTULO 7:", "CAPÍTULO 10:")
    part2 = part2.replace("Capítulo 7:", "Capítulo 10:")
    part2 = part2.replace("7. CONCLUSIONES Y RECOMENDACIONES", "10. CONCLUSIONES Y RECOMENDACIONES")
    part2 = part2.replace("7.1 Conclusiones", "10.1 Conclusiones del Prototipo")
    part2 = part2.replace("7.2 Recomendaciones", "10.2 Recomendaciones del Prototipo")

    part2 = part2.replace("CAPÍTULO 8:", "CAPÍTULO 12:")
    part2 = part2.replace("Capítulo 8:", "Capítulo 12:")
    part2 = part2.replace("8. BIBLIOGRAFÍA", "12. BIBLIOGRAFÍA")
    part2 = part2.replace("8.1 Referencias", "12.1 Referencias")
    part2 = part2.replace("8.2 Documentación", "12.2 Documentación")
    part2 = part2.replace("8.3 Normativa", "12.3 Normativa")

    part2 = part2.replace("CAPÍTULO 9:", "CAPÍTULO 13:")
    part2 = part2.replace("Capítulo 9:", "Capítulo 13:")
    part2 = part2.replace("9. ANEXOS", "13. ANEXOS")

    # Insert new conclusions, recommendations and bibliography before chapter 12
    conclusiones_nuevas = """
    # ========================================================================
    # CAPÍTULO 10.3: CONCLUSIONES ADICIONALES (ECOSISTEMA)
    # ========================================================================
    add_heading_apa(doc, "10.3 Conclusiones sobre el Ecosistema Tecnológico", 2)
    add_paragraph_apa(doc, "Estado actual del ecosistema tecnológico: La Universidad Nacional de Chimborazo (UNACH) ha logrado avances tecnológicos muy significativos a lo largo de las últimas dos décadas. Actualmente, la institución cuenta con una infraestructura contemporánea y robusta, destacando el reciente proyecto \\"Backbone de Redes de Telecomunicaciones\\" en el campus norte, el cual implementó tecnología de punta con inteligencia artificial (Juniper Mist) para garantizar una conectividad de alta disponibilidad. Asimismo, la universidad gestiona de forma operativa sus procesos mediante plataformas académicas sólidamente establecidas, como el Sistema Informático de Control Académico (SICOA) y Moodle, apoyadas por un esquema de seguridad que incluye respaldos inmutables locales y en la nube de CEDIA. Todo esto ha permitido automatizar procesos, agilizar trámites y garantizar la continuidad educativa frente a crisis.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Nivel de integración de datos: El principal hallazgo respecto al ecosistema de la UNACH es que, si bien existen sistemas funcionales y avanzados, estos operan frecuentemente como \\"islas de digitalización\\" carentes de una articulación integral. El nivel de integración de datos en tiempo real es aún limitado; por ejemplo, la extracción de registros masivos para analizar el aprendizaje (desde SICOA y Moodle) depende de la entrega de archivos estáticos en formatos CSV o Excel por parte de las dependencias técnicas. Sin embargo, la institución ha logrado un avance importante en materia de protección al consolidar la integración de datos mediante un identificador único anonimizado o seudonimizado, el cual permite cruzar información longitudinal y correlacionalmente entre plataformas sin vulnerar la privacidad de los estudiantes.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Principales problemas encontrados: La investigación y los reportes institucionales evidencian que los retos abarcan dimensiones tanto técnicas como culturales: 1) Falta de planificación centralizada. 2) Factores económicos y operativos. 3) Resistencia cultural y brecha digital.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Potencial del modelo UNACH-LA: El proyecto \\"Modelo UNACH-LA de Learning Analytics\\" representa una oportunidad estratégica para superar las barreras de las \\"islas de digitalización\\" mediante la integración de dimensiones pedagógicas, tecnológicas y éticas. El gran potencial de este modelo radica en su capacidad para transformar los volúmenes crecientes de datos educativos masivos (historiales y huella digital) en conocimiento accionable. Al generar un prototipo funcional basado en tableros de control (dashboards) institucionales, el sistema dotará a las autoridades y docentes de indicadores clave de desempeño en tiempo real. A largo plazo, el modelo UNACH-LA permitirá tomar decisiones basadas en evidencia para reducir el riesgo de deserción estudiantil y mejorar el rendimiento académico. Además, servirá como catalizador para la formación del personal (proyectando capacitar a más de 50 docentes y gestores en analítica educativa), lo que facilitará una verdadera adopción tecnológica y alineará a la universidad con las exigencias de la nueva \\"Política Pública para la Transformación Digital del Ecuador 2025-2030\\".", indent=True, color=ROJO)
    
    # ========================================================================
    # CAPÍTULO 11: RECOMENDACIONES ESTRATÉGICAS
    # ========================================================================
    print("  >> Capítulo 11: Recomendaciones Estratégicas...")
    add_heading_apa(doc, "11. RECOMENDACIONES ESTRATÉGICAS INSTITUCIONALES", 1)
    add_paragraph_apa(doc, "Con base en el diagnóstico de la infraestructura, los flujos de información y el marco normativo de la Universidad Nacional de Chimborazo (UNACH), se establecen las siguientes recomendaciones estratégicas:", indent=True, color=ROJO)
    
    add_heading_apa(doc, "11.1 Mejoras tecnológicas", 2)
    add_paragraph_apa(doc, "Escalabilidad y modernización: Se recomienda sostener y expandir el reciente proyecto de modernización \\"Backbone de Redes de Telecomunicaciones\\" (que utiliza tecnología de inteligencia artificial Juniper Mist) hacia todas las áreas y campus, garantizando un soporte técnico reducido y una alta disponibilidad de conexión.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Actualización de sistemas centrales: Es fundamental asignar presupuesto para la actualización de librerías de software institucional (como IronPDF), necesarias para la generación eficiente de reportes en formatos PDF integrados a los sistemas actuales.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Transición a la nube: Mantener una infraestructura tecnológica flexible y escalable, continuando con la migración gradual hacia tecnologías en la nube, lo cual complementará los servidores físicos del Data Center y asegurará la continuidad de los servicios digitales ante cualquier eventualidad.", indent=True, color=ROJO)
    
    add_heading_apa(doc, "11.2 Integración de plataformas", 2)
    add_paragraph_apa(doc, "Erradicar las \\"islas de digitalización\\": Se debe superar el modelo actual donde las plataformas operan de forma aislada. Es imperativo que los productos tecnológicos confluyan en un objetivo único y articulado.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Automatización mediante APIs: Reemplazar el intercambio manual de datos (mediante archivos estáticos CSV o Excel proporcionados por la DTIC y CODESI) por el desarrollo de conectores automatizados (APIs) en tiempo real que enlacen los registros del Sistema Informático de Control Académico (SICOA) con la huella digital del Aula Virtual (Moodle).", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Cumplimiento de interoperabilidad: Alinear la arquitectura de software institucional con el eje estratégico de \\"Interoperabilidad\\" exigido por la Política Pública para la Transformación Digital del Ecuador 2025-2030.", indent=True, color=ROJO)

    add_heading_apa(doc, "11.3 Implementación de analítica de aprendizaje", 2)
    add_paragraph_apa(doc, "Ejecución del Modelo UNACH-LA: Priorizar y dotar de los recursos necesarios para el desarrollo e implementación del \\"Modelo UNACH-LA de Learning Analytics\\", el cual permitirá transformar los crecientes volúmenes de datos masivos en conocimiento accionable.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Desarrollo de Dashboards institucionales: Construir un prototipo funcional basado en tableros de control (dashboards) que proyecten indicadores clave de desempeño (KPIs) en tiempo real, enfocados en predecir el rendimiento académico y alertar sobre el riesgo de deserción estudiantil.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Capacitación en analítica educativa: Para garantizar que el modelo no sea solo una herramienta técnica, se recomienda cumplir con la meta de formar al menos a 50 docentes y gestores universitarios en analítica del aprendizaje. Esto permitirá que las autoridades y tutores interpreten correctamente los datos y apliquen intervenciones pedagógicas oportunas.", indent=True, color=ROJO)

    add_heading_apa(doc, "11.4 Estrategias de gobernanza de datos", 2)
    add_paragraph_apa(doc, "Creación de un Plan Específico de Transformación Digital: La principal recomendación a nivel gerencial es diseñar y formalizar un \\"Plan de Transformación Digital\\" específico. Actualmente, la digitalización figura solo como un eje transversal, lo que limita su efectividad. Un plan estructurado a largo plazo garantizará el compromiso de las autoridades y la asignación eficiente de recursos presupuestarios.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Protección y anonimización: Fortalecer las políticas de seguridad de la información (basadas en normas como ISO 27001 y la Ley Orgánica de Protección de Datos Personales). Se debe mantener como política innegociable la anonimización y seudonimización de los datos académicos mediante identificadores únicos no reversibles, asegurando que los cruces de bases de datos para analítica no expongan la identidad de los estudiantes.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Gestión del cambio y cultura digital: La gobernanza no solo debe centrarse en los datos, sino en las personas. Se recomienda fortalecer los programas de capacitación continua para docentes y personal administrativo como herramienta clave para vencer la resistencia cultural al cambio y reducir la brecha digital, demostrando los beneficios tangibles que la digitalización aporta a sus labores diarias.", indent=True, color=ROJO)
    add_paragraph_apa(doc, "Fortalecimiento del EGSI y CSIRT: Consolidar el rol del Equipo de Gestión de Seguridad de la Información (EGSI) y del Equipo de Respuesta a Incidentes (CSIRT) para el monitoreo permanente, la auditoría de accesos y la actualización de los planes de contingencia frente a posibles vulnerabilidades tecnológicas.", indent=True, color=ROJO)
    doc.add_page_break()
    """

    # We need to insert `conclusiones_nuevas` right before "    doc.add_page_break()\n\n    # ========================================================================\n    # CAPÍTULO 12: BIBLIOGRAFÍA"
    cap12_marker = "    # ========================================================================\n    # CAPÍTULO 12: BIBLIOGRAFÍA"
    parts2 = part2.split(cap12_marker)
    if len(parts2) == 2:
        parts2[0] = parts2[0] + "\n" + conclusiones_nuevas + "\n"
        part2 = cap12_marker.join(parts2)
    
    # We also need to add new bibliography entries in RED
    new_biblio = """
    nuevas_referencias = [
        "Universidad Nacional de Chimborazo. (2020). HERRAMIENTAS DIGITALES PARA TU COMODIDAD. Gaceta Universitaria.",
        "Vicerrectorado Administrativo - UNACH. (2023). INFORME BIMESTRAL DE ACTIVIDADES MACROPROCESO GESTIÓN ADMINISTRATIVA: Gestión de Tecnologías de la Información y Comunicación. Periodo 01/11/2022 al 31/12/2022.",
        "Universidad Nacional de Chimborazo. (2023). LOS NUEVOS LABORATORIOS DE INGENIERÍA: OTRA OBRA EN MOVIMIENTO. Noticias - Facultad de Ingeniería.",
        "Universidad Nacional de Chimborazo. (2019). La infraestructura contemporánea es un hito de la Unach. Noticias Institucionales.",
        "Centro de Tecnología Educativa - UNACH. (2018). POLITICAS DE SEGURIDAD DE INFORMACION UNACH 2018.",
        "Paredes Barrigas, S. L., & Negrete Costales, O. P. (2025). Políticas públicas para la transformación digital en el sector público: un estudio de caso en la Universidad Nacional de Chimborazo. Revista Esprint Investigación, 4(1), 498-514.",
        "Comisión de Investigación, Innovación y Vinculación - UNACH. (2026). Requerimiento_Datos_Proyecto_ModeloLA-signed.pdf (Resolución No. 037-CIV-12-02-2026).",
        "Dirección de Tecnologías de la Información y Comunicación (DTIC). Servicios - Dirección de Tecnologías de la Información y Comunicación. Universidad Nacional de Chimborazo.",
        "Coordinación de Desarrollo de Sistemas Informáticos (CODESI). Sistema Informático de Control Académico – Sicoa | Documentación.",
        "Universidad Nacional de Chimborazo. (2025). Tecnología alemana impulsa la innovación en la Facultad de Ingeniería de la Unach. Noticias Academia y Gestión.",
        "Universidad Nacional de Chimborazo. (2024). Unach moderniza su infraestructura con proyecto de telecomunicaciones avanzado. Noticias Institucionales."
    ]
    for ref in nuevas_referencias:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(ref)
        run.font.size = Pt(10)
        run.font.color.rgb = ROJO
"""
    # Insert new biblio after existing
    refs_marker = "    for ref in referencias:\n        p = doc.add_paragraph()\n        p.paragraph_format.left_indent = Cm(1.27)\n        p.paragraph_format.first_line_indent = Cm(-1.27)\n        p.paragraph_format.space_after = Pt(6)\n        run = p.add_run(ref)\n        run.font.size = Pt(10)\n        run.font.color.rgb = GRIS_OSCURO\n"
    parts3 = part2.split(refs_marker)
    if len(parts3) == 2:
        parts3[0] = parts3[0] + refs_marker + "\n" + new_biblio + "\n"
        part2 = parts3[0] + parts3[1]
    
    new_content = part1 + new_sections + cap5_marker + part2
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Patch applied successfully.")
else:
    print("Could not find the insertion marker.")
