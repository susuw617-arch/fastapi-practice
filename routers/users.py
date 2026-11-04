from unittest import result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import UserTable
from schemas import User, UserOut

router = APIRouter(prefix="/users", tags=["用户"])



#增：新增用户
@router.post("")
async def add_user(user:User,db:AsyncSession = Depends(get_db)):
    new_user = UserTable(name=user.name,age=user.age)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"message":"添加成功","id":new_user.id}


#查：一个用户
@router.get("/{user_id}",response_model=UserOut)
async def get_user(user_id:int,db:AsyncSession = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404,detail="用户不存在")
    return user

#改
@router.put("/{user_id}")
async def change_user(user_id:int,user:User,db:AsyncSession = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user_id)
    result = await db.execute(stmt)
    sql_user = result.scalar_one_or_none()
    if sql_user:
        sql_user.name = user.name
        sql_user.age = user.age
    else:
        raise HTTPException(status_code=404, detail="用户不存在")
    await db.commit()
    return {"message":"修改成功!"}

#删
@router.delete("/{user_id}")
async def delete_user(user_id: int,db: AsyncSession = Depends(get_db)):
    stmt = select(UserTable).where(UserTable.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")


    await db.delete(user)
    await db.commit()
    return {"message": "删除成功!"}


@router.get("",response_model=list[UserOut])
async def list_user(page:int = 1,size: int = 10,db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * size
    stmt = select(UserTable).offset(offset).limit(size)
    result = await db.execute(stmt)
    return result.scalars().all()

