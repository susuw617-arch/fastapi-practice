from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, UserTable


# 每次请求开一个数据库会话，用完自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 增：新增用户
@app.post("/users")
def add_user(user: User, db: Session = Depends(get_db)):
    new_user = UserTable(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "添加成功", "id": new_user.id}


# 查：所有用户
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserTable).all()


# 查：一个用户
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
