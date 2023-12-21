from fastapi import FastAPI, HTTPException
import models

from database import SessionLocal, Base, engine

app = FastAPI()

Base.metadata.create_all(engine)

session = SessionLocal()

person_repo = models.PersonRepository(session, models.Person)
region_repo = models.RegionRepository(session, models.Region)

@app.post("/regions/create/{region_name}")
def create_region(region_name: str):
    region = region_repo.get_by_name(region_name)
    if region:
        raise HTTPException(status_code=400, detail="Регион успешно создан")

    new_region = models.Region(name=region_name)
    region_repo.create(new_region)
    return {"message": "Регион успешно создан"}

# Добавление человека с заданным регионом
@app.post("/people/with_region/{fio}/{sex}/{region_name}")
def create_person_with_region(fio: str, sex: str, region_name: str):
    region = region_repo.get_by_name(region_name)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    person = models.Person(fio=fio, sex=sex, region_id=region.id)
    person_repo.create(person)
    return {"message": "Человек с заданным регионом успешно добавлен"}

@app.post("/people/without_region/{fio}/{sex}")
def create_person_without_region(fio: str, sex: str):
    person = models.Person(fio=fio, sex=sex)
    person_repo.create(person)
    return {"message": "Человек без принадлежности к региону успешно добавлен"}

@app.get("/people")
def get_all_people():
    people = person_repo.get_all()
    return {"people": people}

@app.get("/regions")
def get_regions():
    regions = region_repo.get_all()
    return { "regions" : regions}

@app.get("/regions/{region_name}/people")
def get_people_in_region(region_name: str):
    region = region_repo.get_by_name(region_name)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    people = person_repo.get_by_region_id(region.id)
    return {"people": people}

@app.put("/people/{person_fio}/move/{region_name}")
def relocate_person(person_fio: str, region_name: str):
    person = person_repo.get_by_name(person_fio)
    if not person:
        raise HTTPException(status_code=404, detail="Человек с таким именем не найден")
    region = region_repo.get_by_name(region_name)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    person_repo.update_region(person, region.id)
    return {"message": "Человек успешно переселен в другой регион"}


@app.put("/people/{old_fio}/change_name/{new_fio}")
def change_person_name(old_fio: str, new_fio: str):
    person = person_repo.get_by_name(old_fio)
    if not person:
        raise HTTPException(status_code=404, detail="Человек с таким именем не найден")
    person_repo.update_name(person, new_fio)
    return {"message": "ФИО человека успешно изменено"}

# Выселение человека из региона
@app.put("/people/{fio}/evict")
def deport_person(fio: str):
    person = person_repo.get_by_name(fio)
    if not person:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person_repo.update_region(person, None)
    return {"message": "Человек был успешно выселен из региона"}

# Удаление человека
@app.delete("/people/{fio}/delete")
def delete_person_by_name(fio: str):
    person = person_repo.get_by_name(fio)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person_repo.delete(person)
    return {"message": "Человек успешно удален"}


# Удаление региона
@app.delete("/regions/{region_name}/delete/{cascade}")
def delete_region(region_name: str, cascade: bool):
    region = region_repo.get_by_name(region_name)
    if not region:
        raise HTTPException(status_code=404, detail="Регион не найден")
    if not cascade:
        for person in region.citizens:
            person.region = None

    region_repo.delete(region)
    return {"message": "Region successfully deleted"}
