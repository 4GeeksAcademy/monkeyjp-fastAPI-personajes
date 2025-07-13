from pydantic import BaseModel
from typing import List, Optional

# -------- PERSONAJE --------

class PersonajeBase(BaseModel):
    nombre: str
    frase: str
    imagen: str
    usuario_id: int


class PersonajeCreate(PersonajeBase):
    pass

class PersonajeUpdate(PersonajeBase):
    pass

class PersonajeOut(PersonajeBase):
    id: int

    class Config:
        orm_mode = True

# -------- USUARIO --------

class UsuarioBase(BaseModel):
    nombre: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int
    personajes: List[PersonajeOut] = []

    class Config:
        orm_mode = True
