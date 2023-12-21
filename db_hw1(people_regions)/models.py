from database import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import ForeignKey

class Region(Base):
    __tablename__ = "regions"

    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    citizens: Mapped[List["Person"]] = relationship(back_populates="region")

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column(String(30))
    sex: Mapped[str] = mapped_column(String(30))
    region_id = mapped_column(ForeignKey("regions.id"), nullable = True)

    region: Mapped[Region] = relationship(back_populates="citizens")


