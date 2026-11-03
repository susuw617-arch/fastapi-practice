from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def hello_world(name: str):
    return {"message": f"Hello {name}"}

@app.get("/add")
async def add(a: int, b: int) -> int:
    return a + b

@app.post("/user")
async def create_user(user:User):
    return {f"message:创建成功{user.name}"}


