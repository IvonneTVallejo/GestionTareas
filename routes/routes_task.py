from telnetlib import ENCRYPT
from unittest import result
from fastapi import APIRouter, Response
from sqlalchemy import and_
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.task import TaskSchema
from config.db import engine
from model.task import tasks
from typing import List


task = APIRouter()


# Crear tarea
@task.post("/api/task", status_code=HTTP_201_CREATED)
def create_task(data_task: TaskSchema):
    with engine.connect() as conn:
        new_task = data_task.dict()
        conn.execute(tasks.insert().values(new_task))
        return Response(status_code=HTTP_201_CREATED)


# Editar tarea
@task.put("/api/task/{task_id}", response_model=TaskSchema)
def update_task(data_update: TaskSchema, task_id: str):
    with engine.connect() as conn:
        conn.execute(tasks.update().values(name=data_update.name, description=data_update.description,
                     idUser=data_update.idUser).where(tasks.c.id == task_id))
        result = conn.execute(tasks.select().where(
            tasks.c.id == task_id)).first()
        return result


# Eliminar tarea
@task.delete("/api/task/{task_id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    with engine.connect() as conn:
        conn.execute(tasks.delete().where(tasks.c.id == task_id))
        return Response(status_code=HTTP_204_NO_CONTENT)


# Consultar una tarea de un usuario
@task.get("/api/task/{user_id}/{task_id}", response_model=TaskSchema)
def get_tasks(user_id: str, task_id: str):
    with engine.connect() as conn:
        result = conn.execute(tasks.select().where(
            and_(tasks.c.idUser == user_id, tasks.c.id == task_id))).first()
        return result


# Consultar todas las tareas de un usuario
@task.get("/api/task/{user_id}", response_model=List[TaskSchema])
def get_tasks(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(tasks.select().where(
            tasks.c.idUser == user_id)).fetchall()
        return result
