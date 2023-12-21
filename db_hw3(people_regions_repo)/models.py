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

    citizens: Mapped[List["Person"]] = relationship(back_populates="region", cascade="delete")

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str] = mapped_column(String(30))
    sex: Mapped[str] = mapped_column(String(30))
    region_id = mapped_column(ForeignKey("regions.id"), nullable = True)

    region: Mapped[Region] = relationship(back_populates="citizens")


class GenericRepository:
    def __init__(self, session, model):
        self.model = model
        self.session = session
    
    def create(self, object):
        self.session.add(object)
        self.session.commit()
    
    def delete(self, object):
        self.session.delete(object)
        self.session.commit()

    def get_all(self):
        return self.session.query(self.model).all()
    
class PersonRepository(GenericRepository):
    def __init__(self, session, person : Person):
        super().__init__(session, person)

    def update_region(self, person, region_id):
        person.region_id = region_id
        self.session.commit()

    def update_name(self, person, edit_fio):
        person.fio = edit_fio
        self.session.commit()

    def get_by_name(self, fio):
        return self.session.query(Person).filter(Person.fio == fio).first()

    def get_by_region_id(self, region_id):
        return self.session.query(Person).filter(Person.region_id == region_id).all()

class RegionRepository(GenericRepository):
    def __init__(self, session, region : Region):
        super().__init__(session, region)

    def get_by_name(self, name):
        return self.session.query(Region).filter(Region.name == name).first()

    def update(self, region, new_name):
        region.name = new_name
        self.session.commit()