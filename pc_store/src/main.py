import uvicorn
from fastapi import FastAPI

from views import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get("/")
def hello_world():
    return {
        "message": "Hello World!"
    }


if __name__ == "__main__":
    uvicorn.run(app)
