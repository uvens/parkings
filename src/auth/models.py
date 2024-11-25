import sqlalchemy as sa
from src.core.models import Base, TrackableMixin
from src.auth.schemas import UserSchema




class User(Base, TrackableMixin):
    __pydantic_model__ = UserSchema

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), nullable=False)
    number = sa.Column(sa.String(length=255), unique=True)
    password = sa.Column(sa.String(length=255), nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=True)

    def __str__(self):
        return self.name



# @register(User, sqlalchemy_sessionmaker=async_session)
# class UserAdmin(SqlAlchemyModelAdmin):
#     exclude = ("password",)
#     list_display = ("id", "name", "number", "is_super_user", "is_active")
#     list_display_links = ("id", "name", "number")
#     list_filter = ("id", "name", "number", "is_super_user", "is_active")
#     search_fields = ("name", "number")
#
#     async def authenticate(self, username, password):
#         sessionmaker = self.get_sessionmaker()
#         async with sessionmaker() as session:
#             query = select(self.model_cls).filter_by(name=username, password=password, is_super_user=True)
#             result = await session.scalars(query)
#             user = result.first()
#             if not user:
#                 return None
#             user_password = user.password
#             if not password == user_password:
#                 return None
#             return user.id
