from asyncfastgeek.db_models import User
from asyncfastgeek.db import async_session
from asyncfastgeek.schemas import CreateUSer, OutUser, UpdateUser
from sqlalchemy import select

async def create_user(createuser: CreateUSer):
    async with async_session() as session:
        users = User(name=createuser.name,email=createuser.email)
        session.add(users)
        await session.commit()

async def get_user(user_id: int) -> OutUser:
    async with async_session() as session:
        user = await session.get(User, user_id)
        return user 

async def list_users() -> list[OutUser]:
    async with async_session() as session:
        stmt = select(User)
        users = await session.scalars(stmt)
        return users.all()

async def update_users(user_id: int, newdata: UpdateUser) -> CreateUSer:
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user:
            user.name = newdata.name or user.name 
            user.email = newdata.email or user.email
            await session.commit()
        return user

async def delete_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user:
            await session.delete(user)
            await session.commit()
        