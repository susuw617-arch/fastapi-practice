from pydantic import BaseModel


class User(BaseModel):
    name : str
    age : int


class UserOut(BaseModel):
    id : int
    name : str
    age : int

    model_config = {"from_attributes":True}

