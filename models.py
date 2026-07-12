from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)

    personajes = relationship(
        "Personaje",
        back_populates="usuario_rel",
        cascade="all, delete-orphan"
    )

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    frase = Column(String, nullable=False)
    imagen = Column(String, nullable=False)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    usuario_rel = relationship("Usuario", back_populates="personajes")