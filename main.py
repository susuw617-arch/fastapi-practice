from fastapi import FastAPI
from database import engine, Base

from contextlib import asynccontextmanager
import models  # 导入一下，建表时才能找到 UserTable
from routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：表不存在就建
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时要做的事写在这里（现在没有）


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)




