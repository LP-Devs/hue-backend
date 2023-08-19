from bson import ObjectId
from pydantic import BaseModel, Field

from src.model.object_id import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"username": "Jane Doe"}}


class UserDBModel(UserModel):
    hashed_password: str
