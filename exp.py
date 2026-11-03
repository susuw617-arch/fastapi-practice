from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, UserTable


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


@app.post("/users")
async def add_user(user: User, db: AsyncSession = Depends(get_db)):
    new_user = UserTable(name=user.name, age=user.age)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message": "添加成功", "id": new_user.id}


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable))
    return result.scalars().all()


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
