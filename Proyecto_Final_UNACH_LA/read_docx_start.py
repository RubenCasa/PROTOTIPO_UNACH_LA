import docx
import sys

try:
    doc = docx.Document('INFORME_FINAL_COMPLETO_UNACH_LA_Actualizado.docx')
except Exception as e:
    print(f"Error abriendo documento: {e}")
    sys.exit(1)

for i, p in enumerate(doc.paragraphs[20:60]):
    print(f"{i+20}: {p.text.strip()}")
