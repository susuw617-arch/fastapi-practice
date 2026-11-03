from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#定义一张表
class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50))
    age = Column(Integer)


#自动建表
Base.metadata.create_all(bind=engine)
