from fastapi import FastAPI, HTTPException
import models

from database import SessionLocal, Base, engine

app = FastAPI()

Base.metadata.create_all(engine)

session = SessionLocal()

# Добавление человека с заданным регионом
@app.post("/people/with_region")
def add_person_with_region(fio_: str, sex_: str, region_id: int):
    region = session.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    person = models.Person(fio = fio_, sex=sex_, region=region)
    session.add(person)
    session.commit()
    return {"message": "Человек с заданным регионом успешно добавлен"}


# Добавление человека с нулевым регионом
@app.post("/people/without_region")
def create_person_without_region(fio_: str, sex_: str):
    person = models.Person(fio=fio_, sex=sex_)
    session.add(person)
    session.commit()
    return {"message": "Человек без принадлежности к региону успешно добавлен"}

@app.put("/people/{person_id}/move")
def relocate_person(person_id : int, region_id : int):
    person_to_relocate = session.query(models.Person).filter(models.Person.id == person_id).first()
    if (not person_to_relocate):
        raise HTTPException(status_code=404, detail="Человек не найден")
    
    person_region = session.query(models.Region).filter(models.Region.id == region_id)
    if (not person_region):
        raise HTTPException(status_code=404, detail="Такой регион не найден")
    
    person_to_relocate.region_id = region_id
    session.commit()
    return {"message" : "Человек успешно переселен в другой регион"}

# Изменить ФИО человека
@app.put("/people/{person_id}/change_name")
def change_person_name(person_id: int, fio: str):
    person = session.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person.fio = fio
    session.commit()
    return {"message": "ФИО человека успешно изменено"}

@app.get("/regions")
def get_regions():
    regions = session.query(models.Region).all()
    return { "regions" : regions}


@app.get("/regions/{region_id}/people")
def get_people_from_region(region_id : int):
    region = session.query(models.Region).filter(models.Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail="регион не найден")
    
    people = session.query(models.Person).filter(models.Person.region_id == region_id).all()
    return { "people" : people}

@app.get("/people_in_regions")
def get_people_from_all_regions():
    people = session.query(models.Person).all()
    return { "people" : people }

# Выселение человека из региона
@app.put("/people/{person_id}/evict")
def deport_person(person_id: int):
    person = session.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person.region_id = None
    session.commit()
    return {"message": "Человек успешно выселен из региона"}

# Удаление человека
@app.delete("/people/{person_id}")
def delete_person(person_id: int):
    person = session.query(models.Person).filter(models.Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    session.delete(person)
    session.commit()
    return {"message": "Человек успешно удален"}
