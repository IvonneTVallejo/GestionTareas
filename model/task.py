from asyncio import tasks
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

tasks = Table("tasks", meta_data,
              Column("id", Integer, primary_key=True),
              Column("name", String(255), nullable=False),
              Column("description", String(255), nullable=False),
              Column("idUser", Integer, nullable=False))

meta_data.create_all(engine)