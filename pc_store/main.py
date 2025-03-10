from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api_v1 import router as router_v1
from core import db_helper, settings
from models import Base


# from pc_store.src.controllers.product_controller import router as product_router
# from pc_store.src.controllers.user_controller import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


# app.include_router(users_router)


# app.include_router(product_router)


@app.get("/")
def hello_world():
    return {
        "message": "Hello World!"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
