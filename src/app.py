from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from src.routes import router
from src.setting import setting as settings
from src.utils import load_all_models
from src.db_connect import check_db_connected, check_db_disconnected
from src.db import async_postgres_dsn

from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin


def include_router(application: FastAPI) -> None:
    application.include_router(router)


def add_middleware(application: FastAPI, *args, **kwargs) -> None:  # noqa
    application.add_middleware(
        *args,
        **kwargs
    )


def start_application() -> FastAPI:
    application = FastAPI(title='parking', debug=settings.debug)
    include_router(application)
    add_pagination(application)
    add_middleware(
        application,
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    return application


app = start_application()





@app.on_event('startup')
async def startup() -> None:
    load_all_models()
    await check_db_connected()



@app.on_event('shutdown')
async def shutdown() -> None:
    await check_db_disconnected()

