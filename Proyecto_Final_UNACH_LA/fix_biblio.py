# -*- coding: utf-8 -*-
import re

file_path = "generar_informe_word.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_refs = re.search(r"nuevas_referencias = \[.*?\]", content, re.DOTALL).group(0)

new_refs = '''nuevas_referencias = [
        "Centro de Tecnología Educativa - UNACH. (2018). Políticas de seguridad de la información UNACH 2018.",
        "Comisión de Investigación, Innovación y Vinculación - UNACH. (2026). Requerimiento de datos para el Proyecto Modelo UNACH-LA (Resolución No. 037-CIV-12-02-2026).",
        "Coordinación de Desarrollo de Sistemas Informáticos (CODESI). (s.f.). Sistema Informático de Control Académico – Sicoa | Documentación.",
        "Dirección de Tecnologías de la Información y Comunicación (DTIC). (s.f.). Servicios - Dirección de Tecnologías de la Información y Comunicación. Universidad Nacional de Chimborazo.",
        "Paredes Barrigas, S. L., & Negrete Costales, O. P. (2025). Políticas públicas para la transformación digital en el sector público: un estudio de caso en la Universidad Nacional de Chimborazo. Revista Esprint Investigación, 4(1), 498-514.",
        "Universidad Nacional de Chimborazo. (2019). La infraestructura contemporánea es un hito de la Unach. Noticias Institucionales.",
        "Universidad Nacional de Chimborazo. (2020). Herramientas digitales para tu comodidad. Gaceta Universitaria.",
        "Universidad Nacional de Chimborazo. (2023). Los nuevos laboratorios de ingeniería: Otra obra en movimiento. Noticias - Facultad de Ingeniería.",
        "Universidad Nacional de Chimborazo. (2024). Unach moderniza su infraestructura con proyecto de telecomunicaciones avanzado. Noticias Institucionales.",
        "Universidad Nacional de Chimborazo. (2025). Tecnología alemana impulsa la innovación en la Facultad de Ingeniería de la Unach. Noticias Academia y Gestión.",
        "Vicerrectorado Administrativo - UNACH. (2023). Informe bimestral de actividades macroproceso gestión administrativa: Gestión de Tecnologías de la Información y Comunicación. Periodo 01/11/2022 al 31/12/2022."
    ]'''

new_content = content.replace(old_refs, new_refs)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
