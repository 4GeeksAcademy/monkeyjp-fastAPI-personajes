from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
import schemas
from models import Usuario, Personaje
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/personajes", response_model=list[schemas.PersonajeOut], tags=["Personajes"])
def get_personajes(db: Session = Depends(get_db)):
    return crud.obtener_personajes(db)

@app.post("/personajes", response_model=schemas.PersonajeOut, tags=["Personajes"])
def add_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    return crud.crear_personaje(db, personaje)

@app.put("/personajes/{id}", response_model=schemas.PersonajeOut, tags=["Personajes"])
def update_personaje(id: int, datos: schemas.PersonajeUpdate, db: Session = Depends(get_db)):
    personaje = crud.actualizar_personaje(db, id, datos)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje

@app.delete("/personajes/{id}", tags=["Personajes"])
def delete_personaje(id: int, db: Session = Depends(get_db)):
    personaje = crud.eliminar_personaje(db, id)
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return {"msg": "Personaje eliminado"}

# -------- USUARIOS --------

@app.post("/usuarios", response_model=schemas.UsuarioOut, tags=["Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.crear_usuario(db, usuario)

@app.get("/usuarios", response_model=list[schemas.UsuarioOut], tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    return crud.obtener_usuarios(db)
