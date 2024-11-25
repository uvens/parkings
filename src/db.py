from typing import AsyncGenerator, Generator

import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool

from src.setting import setting as settings

postgres_url = (
    f'{settings.db_app_user}:{settings.db_app_password}@{settings.db_app_host}:'
    f'{settings.db_app_port}/{settings.dp_app_name}'
)

postgres_dsn = f'postgresql://{postgres_url}'
async_postgres_dsn = f'postgresql+asyncpg://{postgres_url}'

engine = sqlalchemy.create_engine(postgres_dsn, echo=settings.echo)

async_pool_settings = {
    'pool_size': settings.async_pg_pool_size,
    'max_overflow': 10,
    'pool_pre_ping': True,
    'pool_recycle': 1200,
}

async_engine = create_async_engine(
    async_postgres_dsn,
    echo=settings.echo,
    poolclass=AsyncAdaptedQueuePool,
    **async_pool_settings
)

sync_session = sessionmaker(engine, expire_on_commit=False)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


def get_db_session() -> Generator:
    session = sync_session()
    try:
        yield session
    finally:
        session.close()


# async Session dependency
async def get_async_db_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session
