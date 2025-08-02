from sqlalchemy.orm import Session
from models import Personaje, Usuario
from schemas import PersonajeCreate, PersonajeUpdate, UsuarioCreate

# -------- PERSONAJES --------

def obtener_personajes_por_usuario(db: Session, usuario: str):
    return db.query(Personaje).filter(Personaje.usuario == usuario).all()

def obtener_personajes_por_usuario(db: Session, nombre_usuario: str):
    usuario = obtener_usuario_por_nombre(db, nombre_usuario)
    if not usuario:
        return None
    return db.query(Personaje).filter(Personaje.usuario_id == usuario.id).all()

def obtener_personaje_de_usuario(db: Session, nombre_usuario: str, personaje_id: int):
    usuario = obtener_usuario_por_nombre(db, nombre_usuario)
    if not usuario:
        return None
    return db.query(Personaje).filter(
        Personaje.id == personaje_id,
        Personaje.usuario_id == usuario.id
    ).first()

def crear_personaje_para_usuario(db: Session, nombre_usuario: str, personaje: PersonajeCreate):
    usuario = obtener_usuario_por_nombre(db, nombre_usuario)
    if not usuario:
        return None
    nuevo = Personaje(**personaje.dict(), usuario_id=usuario.id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar_personaje_de_usuario(db: Session, nombre_usuario: str, personaje_id: int, datos: PersonajeUpdate):
    personaje = obtener_personaje_de_usuario(db, nombre_usuario, personaje_id)
    if not personaje:
        return None
    for key, value in datos.dict().items():
        setattr(personaje, key, value)
    db.commit()
    db.refresh(personaje)
    return personaje

def eliminar_personaje_de_usuario(db: Session, nombre_usuario: str, personaje_id: int):
    personaje = obtener_personaje_de_usuario(db, nombre_usuario, personaje_id)
    if not personaje:
        return None
    db.delete(personaje)
    db.commit()
    return personaje

# -------- USUARIOS --------

def crear_usuario(db: Session, usuario: UsuarioCreate):
    existente = obtener_usuario_por_nombre(db, usuario.nombre)
    if existente:
        return None  # o puedes lanzar una excepción si prefieres

    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def obtener_usuario_por_nombre(db: Session, nombre: str):
    return db.query(Usuario).filter(Usuario.nombre == nombre).first()
