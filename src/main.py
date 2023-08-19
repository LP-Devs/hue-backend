import os
from http import HTTPStatus

import motor.motor_asyncio
from fastapi import FastAPI, HTTPException

from src.model.token import TokenModel
from src.model.user import UserModel
from src.service.auth import AuthService
from src.service.user import UserService

hostname = os.environ.get("MONGODB_HOSTNAME", "localhost")
port = os.environ.get("MONGODB_PORT", "27017")
username = os.environ.get("MONGODB_USERNAME", "root")
password = os.environ.get("MONGODB_PASSWORD", "example")
client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{username}:{password}@{hostname}:{port}/?authMechanism=DEFAULT")
db = client.HUE

app = FastAPI()


@app.post("/login", description="Login user", response_model=TokenModel)
async def root(username: str, password: str) -> TokenModel:
    user = await UserService(db).get(username)

    auth_service = AuthService()
    if auth_service.authenticate_user(user, password):
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return TokenModel(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Invalid login information")


@app.get("/", response_description="List all users", response_model=list[UserModel])
async def list_users():
    return await UserService(db).list()
