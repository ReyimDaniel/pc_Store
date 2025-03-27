from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from alembic import router as alembic_router
from core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(router=alembic_router, prefix=settings.alembic_prefix)


@app.get("/")
def hello_world():
    return {
        "message": "Hello World!"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
