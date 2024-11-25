from datetime import timedelta
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """Settings"""

    dp_app_name: str = 'parking'
    db_app_user: str = 'parking'
    db_app_password: str = 'parking'
    db_app_host: str = 'localhost'
    db_app_port: int = 5432

    async_pg_pool_size: int = 5
    echo: bool = True
    debug: bool = False
    secret_key: str = 'SecureParkingAccess2024'
    algorithm: str = "HS256"
    access_token_expire_days: int = 30
    access_token_type: str = 'access'
    refresh_token_type: str = 'refresh'
    access_token_ttl: timedelta = timedelta(minutes=30)
    login_url: str = '/parking/auth/login'
    account_id_ukassa: str = '471442'
    secret_key_ukassa: str = 'test_CA_gaoQSgu_2m5Nodm6DKTd8fqC1nYKbDu8U9MxgOqY'


@lru_cache()
def get_settings() -> Settings:
    return Settings()


setting = get_settings()
