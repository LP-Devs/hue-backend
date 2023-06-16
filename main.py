from http import HTTPStatus

import motor.motor_asyncio
from fastapi import FastAPI, HTTPException

from auth_service import AuthService
from model_token import TokenModel
from model_user import UserDBModel, UserModel

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.HUE

app = FastAPI()


@app.post("/login", description="Login user", response_model=TokenModel)
async def root(username: str, password: str) -> TokenModel:
    user = UserDBModel.parse_obj(await db["user"].find_one({
        "username": username
    }))

    auth_service = AuthService()
    if auth_service.authenticate_user(user, password):
        access_token = auth_service.create_access_token(data={"sub": user.username})
        return TokenModel(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Invalid login information")


@app.get(
    "/", response_description="List all users", response_model=list[UserModel]
)
async def list_users():
    users = await db["user"].find().to_list(1000)
    return users