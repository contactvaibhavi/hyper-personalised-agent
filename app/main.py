from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from api.router import router
from dotenv import load_dotenv

load_dotenv()

from services.db import init_db, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Init lifespan")
    # Need to init db here after all usages of schema are imported
    init_db(engine)
    yield
    print("close")


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

from services.db import DbSession


@app.middleware("http")
async def db_session_middleware(request, call_next):
    response = await call_next(request)
    DbSession.remove()
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
