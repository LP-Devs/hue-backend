from model.user import UserDBModel


class UserService:
    def __init__(self, db) -> None:
        self.db = db

    async def list(self) -> list[UserDBModel]:
        return await self.db["user"].find().to_list(1000)

    async def get(self, username: str) -> UserDBModel:
        return await self.db["user"].find_one({"username": username})
