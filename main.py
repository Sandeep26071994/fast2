from fastapi import Depends, FastAPI,status,HTTPException
from database import Base, engine,SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from typing import List

Base.metadata.create_all(engine)

app=FastAPI()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "todoo"

@app.post("/todo",response_model=schemas.ToDo,status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate,session:Session=Depends(get_session)):
    session=Session(bind=engine,expire_on_commit=False)
    tododb=models.ToDo(task=todo.task)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)
    session.close()
    return tododb

@app.get("/todo/{id}",response_model=schemas.ToDo)
def read_todo(id:int):
    session=Session(bind=engine,expire_on_commit=False)
    todo=session.query(models.ToDo).get(id)
    session.close()
    if not todo:
        raise HTTPException(status_code=404,detail=f"todo item with {id} not found")
    return todo
    
@app.put("/todo/{id}")
def update_todo(id:int,task:str):
    session=Session(bind=engine,expire_on_commit=False)
    todo=session.query(models.ToDo).get(id)
    if todo:
        todo.task=task
        session.commit()
    session.close()

    if not todo:
        raise HTTPException(status_code=404,detail=f"todo item with {id} not found")

@app.delete("/todo/{id}")
def delete_todo(id:int):
    session=Session(bind=engine,expire_on_commit=False)
    todo=session.query(models.ToDo).get(id)
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404,detail=f"todo item with {id} not found")

@app.get("/todo",response_model=List[schemas.ToDo])
def read_todo_list():
    session=Session(bind=engine,expire_on_commit=False)
    todo_list=session.query(models.ToDo).all()
    session.close()
    return todo_list