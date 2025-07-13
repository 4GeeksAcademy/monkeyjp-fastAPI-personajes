from sqlalchemy.orm import Session
from models import Personaje, Usuario
from schemas import PersonajeCreate, PersonajeUpdate, UsuarioCreate

# -------- PERSONAJES --------

def obtener_personajes(db: Session):
    return db.query(Personaje).all()

def obtener_personaje(db: Session, personaje_id: int):
    return db.query(Personaje).filter(Personaje.id == personaje_id).first()

def crear_personaje(db: Session, personaje: PersonajeCreate):
    nuevo = Personaje(**personaje.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_personaje(db: Session, personaje_id: int, datos: PersonajeUpdate):
    personaje = obtener_personaje(db, personaje_id)
    if personaje:
        for key, value in datos.dict().items():
            setattr(personaje, key, value)
        db.commit()
        db.refresh(personaje)
    return personaje

def eliminar_personaje(db: Session, personaje_id: int):
    personaje = obtener_personaje(db, personaje_id)
    if personaje:
        db.delete(personaje)
        db.commit()
    return personaje

# -------- USUARIOS --------

def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()
