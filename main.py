import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from clients.minio import ensure_minio_bucket
from routers.profile import router as profile_router
from routers.users import router as user_router, root_router
import uvicorn


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await ensure_minio_bucket()
    yield


app = FastAPI(lifespan=lifespan)
logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        'Необработанная ошибка при %s %s',
        request.method,
        request.url.path,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'Внутренняя ошибка сервера. Попробуйте повторить запрос позже.'},
    )


@app.get("/")
async def root():
    return {'message': 'Hello World'}

app.include_router(profile_router, prefix='/profile')
app.include_router(user_router, prefix='/users')
app.include_router(root_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
