import json
from bson import json_util
from fastapi import FastAPI
import motor.motor_asyncio

from user import UserModel

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

db = client.hue

app = FastAPI()


@app.get("/login", description="Login user")
async def root(username: str, password: str):
    user = await db["user"].find_one({
        "username": username,
        "password": password
    })


    return json.loads(json_util.dumps(user))


@app.get(
    "/", response_description="List all users", response_model=list[UserModel]
)
async def list_users():
    users = await db["user"].find().to_list(1000)
    return users