from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String
from asyncfastgeek.db import engine

class Base(AsyncAttrs,DeclarativeBase):
    pass

#User Model
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40),nullable=False)
    email: Mapped[str] = mapped_column(String(150),nullable=False,unique=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)