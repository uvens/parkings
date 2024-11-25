import bcrypt
from sqlalchemy import Boolean, Integer, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.auth.models import User

from fastadmin import SqlAlchemyModelAdmin, SqlAlchemyInlineModelAdmin, register

from src.db import async_session, get_async_db_session


@register(User, sqlalchemy_sessionmaker=async_session)
class UserModelAdmin(SqlAlchemyModelAdmin):
    exclude = ("password",)
    list_display = ("id", "name", "is_super_user")
    list_display_links = ("id", "name")
    list_filter = ("id", "name", "is_super_user")
    search_fields = ("name",)

    async def authenticate(self, username, password):
        sessionmaker = self.get_sessionmaker()
        async with sessionmaker() as session:
            query = select(self.model_cls).filter_by(name=username, password=password, is_super_user=True)
            result = await session.scalars(query)
            obj = result.first()
            if not obj:
                return None
            return obj.id

    # async def change_password(self, user_id, password):
    #     sessionmaker = self.get_sessionmaker()
    #     async with sessionmaker() as session:
    #         # use hash password for real usage
    #         query = update(self.model_cls).where(User.id.in_([user_id])).values(password=password)
    #         await session.execute(query)
    #         await session.commit()


from fastapi_amis_admin.admin import ModelAdmin
from src.auth.models import User
from src.db import async_session

class UserAdmin(ModelAdmin):
    page_schema = 'User Admin'  # Название страницы
    model = User  # Модель, которую будем отображать
    engine = async_session  # Подключение к базе данных
    fields = [User.id, User.name, User.number, User.is_active, User.is_super_user]