from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from app.exceptions import UserNotFoundError, UserAlreadyExistsError


class UserService:
    @staticmethod
    async def create_user(user_data: schemas.UserCreate, db: AsyncSession):
        existing = await db.execute(
            select(models.User).where(
                (models.User.username == user_data.username)
                | (models.User.email == user_data.email)
            )
        )
        existing_user = existing.scalar_one_or_none()
        if existing_user:
            field = (
                "username" if existing_user.username == user_data.username else "email"
            )
            raise UserAlreadyExistsError(field, getattr(user_data, field))

        new_user = models.User(username=user_data.username, email=user_data.email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession):
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(user_id)
        return user

    @staticmethod
    async def get_all_users(db: AsyncSession):
        result = await db.execute(select(models.User))
        return result.scalars().all()

    @staticmethod
    async def update_user(user_id: int, user_data: schemas.UserUpdate, db: AsyncSession):
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(user_id)

        if user_data.username:
            user.username = user_data.username
        if user_data.email:
            user.email = user_data.email

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession):
        result = await db.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(user_id)

        await db.delete(user)
        await db.commit()
        return user
