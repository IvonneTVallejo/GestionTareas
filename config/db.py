from venv import create
from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:@localhost:3306/gestionTareas")

meta_data = MetaData()