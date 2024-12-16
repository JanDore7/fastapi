from pydantic import EmailStr
from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.users import UsersOrm
from src.repos.mapper.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        user_with_password = self.mapper.map_to_schema(model)
        return user_with_password
        # return UserWithPassword.model_validate(model)


#
