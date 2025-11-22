from urllib.request import Request

from fastapi import FastAPI

from app.core.config import settings
from app.utils.error import AppBaseError
from app.api import routers

app = FastAPI(
    name="API Virtual Goods",
    description="Виртуальные товары"
)

@app.exception_handler(AppBaseError)
async def shortener_base_error_handler(
        request: Request,
        exc: AppBaseError
):
    raise exc.to_http_exception()

for router in routers:
    app.include_router(router, prefix=settings.api.prefix)