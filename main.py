from fastapi import FastAPI,Depends,HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from database import SessionLocal,UserTable

app = APIRoute

class User(BaseModel):
    id : int
    name : str
    age : int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#增：新增用户
@app.post("/users")
def add_user(user:User,db:Session = Depends(get_db)):
    new_user = UserTable(name=user.name,age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"添加成功","id":new_user.id}


#查：一个用户
@app.get("/users/{user_id}")
def get_user(user_id:int,db:Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="用户不存在")
    return user

#改
@app.put("/users/{user_id}")
def change_user(user:User,db:Session = Depends(get_db)):
    old_user = db.query(UserTable).filter(UserTable.id == user.id).first()
    if not old_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    old_user.name = user.name
    old_user.age = user.age

    db.flush()
    db.commit()

#删
@app.delete("/users/{user_id}")
def detete_user(user:User,db:Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.id == user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.flush()
