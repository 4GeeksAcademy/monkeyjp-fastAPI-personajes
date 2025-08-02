from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
import schemas
from models import Usuario, Personaje
from fastapi.middleware.cors import CORSMiddleware
from schemas import PersonajeCreate, PersonajeUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica ["http://localhost:3000"] si lo prefieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- PERSONAJES --------

@app.get("/usuarios/{nombre}/personajes", tags=["Personajes"])
def listar_personajes(nombre: str, db: Session = Depends(get_db)):
    personajes = crud.obtener_personajes_por_usuario(db, nombre)
    if personajes is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return personajes

@app.post("/usuarios/{nombre}/personajes", tags=["Personajes"])
def crear(nombre: str, personaje: PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = crud.crear_personaje_para_usuario(db, nombre, personaje)
    if nuevo is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return nuevo

@app.get("/usuarios/{nombre}/personajes/{id}", tags=["Personajes"])
def ver_personaje(nombre: str, id: int, db: Session = Depends(get_db)):
    personaje = crud.obtener_personaje_de_usuario(db, nombre, id)
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado para este usuario")
    return personaje

@app.put("/usuarios/{nombre}/personajes/{id}", tags=["Personajes"])
def actualizar(nombre: str, id: int, datos: PersonajeUpdate, db: Session = Depends(get_db)):
    actualizado = crud.actualizar_personaje_de_usuario(db, nombre, id, datos)
    if actualizado is None:
        raise HTTPException(status_code=404, detail="No se pudo actualizar: personaje o usuario no existen")
    return actualizado

@app.delete("/usuarios/{nombre}/personajes/{id}", tags=["Personajes"])
def eliminar(nombre: str, id: int, db: Session = Depends(get_db)):
    eliminado = crud.eliminar_personaje_de_usuario(db, nombre, id)
    if eliminado is None:
        raise HTTPException(status_code=404, detail="No se pudo eliminar: personaje o usuario no existen")
    return eliminado

# -------- USUARIOS --------

@app.post("/usuarios/{nombre}", response_model=schemas.UsuarioOut, tags=["Usuarios"])
def crear_usuario(nombre: str, db: Session = Depends(get_db)):
    usuario_data = schemas.UsuarioCreate(nombre=nombre)
    nuevo_usuario = crud.crear_usuario(db, usuario_data)

    if not nuevo_usuario:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return nuevo_usuario

@app.get("/usuarios", response_model=list[schemas.UsuarioOut], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.obtener_usuarios(db)

@app.get("/usuarios/{nombre}", response_model=schemas.UsuarioOut, tags=["Usuarios"])
def obtener_usuario_por_nombre(nombre: str, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario_por_nombre(db, nombre)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
