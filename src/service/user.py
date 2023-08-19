from src.model.user import UserDBModel, UserModel


class UserService:
    def __init__(self, db) -> None:
        self.db = db

    async def list(self) -> list[UserModel]:
        return await self.db["user"].find().to_list(1000)

    async def get(self, username: str) -> UserDBModel:
        user = await self.db["user"].find_one({"username": username})
        return UserDBModel.parse_obj(user)
