from fastapi import FastAPI,Depends,HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, UserTable


from database import AsyncSessionLocal,UserTable

app = APIRoute

class User(BaseModel):
    id : int
    name : str
    age : int

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

#增：新增用户
@app.post("/users")
async def add_user(user:User,db:AsyncSession = Depends(get_db)):
    new_user = UserTable(name=user.name,age=user.age)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message":"添加成功","id":new_user.id}


#查：一个用户
@app.get("/users/{user_id}")
async def get_user(user_id:int,db:Session = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404,detail="用户不存在")
    return user

#改
@app.put("/users/{user_id}")
async def change_user(user:User,db:Session = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user.id)
    result = await db.execute(stmt)
    sql_user = result.scalar_one_or_none()
    if not sql_user:
        sql_user.name = user.name
        sql_user.age = user.age

    db.flush()
    db.commit()

#删
@app.delete("/users/{user_id}")
async def detete_user(user:User,db:Session = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")


    db.delete(user)
    db.flush()
