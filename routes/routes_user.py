from telnetlib import ENCRYPT
from unittest import result
from click import password_option
from fastapi import APIRouter, Response, Header
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user import UserSchema
from schema.user import DataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from functions_jwt import validate_token, write_token
from fastapi.responses import JSONResponse

user = APIRouter()

# Registrar usuarios nuevos encriptando la contraseña

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["password"] = generate_password_hash(
            data_user.password, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
        return Response(status_code=HTTP_201_CREATED)


# Autenticar usuarios registrados mediante JWT

@user.post("/api/user/login", status_code=200)
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.username == data_user.username)).first()

        if result != None:
            check_passw = check_password_hash(result[4], data_user.password)

            if check_passw:
                return write_token(data_user.dict())
            else:
                return JSONResponse(content={"message": "User not found"}, status_code=404)

        return {
            "status": HTTP_401_UNAUTHORIZED,
            "message": "Access denied"
        }


# Verificar el token generado

@user.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)
