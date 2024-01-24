from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Configuracion CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Ajusta según tu dominio de aplicación Vue.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class Cultivo(BaseModel):
    municipio: str
    vereda: str
    nombre_predio: str
    cultivo_analizado: str
    clima: str
    nombre_cajuela: str
    area_cultivo: float
    coordenadas: str

# Almacenamiento temporal de datos (simula una base de datos)
db = []

# Operaciones CRUD

# Crear un nuevo cultivo
@app.post("/cultivos/", response_model=Cultivo)
def create_cultivo(cultivo: Cultivo):
    db.append(cultivo)
    return cultivo

# Obtener todos los cultivos
@app.get("/cultivos/", response_model=List[Cultivo])
def read_cultivos():
    return db

# Obtener un cultivo por ID
@app.get("/cultivos/{cultivo_id}", response_model=Cultivo)
def read_cultivo(cultivo_id: int):
    if cultivo_id < 0 or cultivo_id >= len(db):
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    return db[cultivo_id]

# Actualizar un cultivo por ID
@app.put("/cultivos/{cultivo_id}", response_model=Cultivo)
def update_cultivo(cultivo_id: int, updated_cultivo: Cultivo):
    if cultivo_id < 0 or cultivo_id >= len(db):
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    
    db[cultivo_id] = updated_cultivo
    return updated_cultivo

# Eliminar un cultivo por ID
@app.delete("/cultivos/{cultivo_id}", response_model=Cultivo)
def delete_cultivo(cultivo_id: int):
    if cultivo_id < 0 or cultivo_id >= len(db):
        raise HTTPException(status_code=404, detail="Cultivo no encontrado")
    
    deleted_cultivo = db.pop(cultivo_id)
    return deleted_cultivo
