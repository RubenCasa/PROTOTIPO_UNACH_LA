from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

app = FastAPI(title="SICOA AI API", description="API Backend para el Dashboard del SICOA de la UNACH")

# Configurar CORS para permitir que React se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción se pondría el dominio de Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentData(BaseModel):
    id_estudiante: str
    carrera: str
    probabilidad_riesgo_ml: float
    semaforo: str
    nivel_riesgo: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API de SICOA UNACH funcionando correctamente."}

@app.post("/api/generar-plan")
async def generar_plan(student: StudentData):
    """
    Simula la llamada a la API de OpenAI/LLM con un retraso de red,
    utilizando los datos reales enviados desde el Dashboard.
    """
    # Simulamos el tiempo de procesamiento de la IA (2 segundos)
    await asyncio.sleep(2)
    
    plan_texto = f"""[SISTEMA IA UNACH-LA: INFORME GENERATIVO DE INTERVENCIÓN]
Evaluando al estudiante ID: {student.id_estudiante} (Carrera: {student.carrera})
Probabilidad de Riesgo Predictiva: {student.probabilidad_riesgo_ml}% ({student.nivel_riesgo})

ANALIZANDO PATRONES...
- Se ha detectado un comportamiento académico anómalo en el semestre actual.
- El modelo XGBoost clasifica este patrón en el semáforo '{student.semaforo}'.

--- PLAN DE ACCIÓN RECOMENDADO ---

1. INTERVENCIÓN TEMPRANA (Próximas 48 Horas):
El Coordinador de Carrera debe citar al estudiante para una tutoría diagnóstica personalizada. 

2. APOYO ACADÉMICO INMEDIATO:
Asignar al estudiante a los talleres de nivelación. Su nivel de riesgo ({student.probabilidad_riesgo_ml}%) requiere seguimiento estricto.

[Fin de la generación del plan. Documento emitido por el modelo predictivo de la UNACH.]"""

    return {"plan": plan_texto}
