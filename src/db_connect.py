import databases
from src.db import async_postgres_dsn


async def check_db_connected() -> None:
    try:
        database = databases.Database(async_postgres_dsn)
        if not database.is_connected:
            await database.connect()
            await database.execute('SELECT 1')
    except Exception as e:
        raise e


async def check_db_disconnected() -> None:
    try:
        database = databases.Database(async_postgres_dsn)
        if database.is_connected:
            await database.disconnect()
    except Exception as e:
        raise e
