from http import HTTPStatus

import motor.motor_asyncio
from fastapi import FastAPI, HTTPException

from model.token import TokenModel
from model.user import UserModel
from service.auth import AuthService
from service.user import UserService

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
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
