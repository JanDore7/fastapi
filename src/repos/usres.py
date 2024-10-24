from pydantic import EmailStr
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithPassword


class UserRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr) -> UserWithPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithPassword.model_validate(model)