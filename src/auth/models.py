from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData

from ..app.models import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
