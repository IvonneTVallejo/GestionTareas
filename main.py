from fastapi import FastAPI
from routes.routes_user import user
from routes.routes_task import task
from dotenv import load_dotenv

app = FastAPI()

app.include_router(user)
app.include_router(task)

load_dotenv()