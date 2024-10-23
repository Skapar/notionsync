from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
