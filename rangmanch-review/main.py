from contextlib import asynccontextmanager
from pydoc import cram
from fastapi import FastAPI
from starlette.types import Lifespan
from database import create_tables
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan Started")
    create_tables()
    print("Database tables created")
    yield
    #shutdown: cleanup here
    print("Shutting down the app")

app = FastAPI(
    title="Rangmanch Reviews API",
    description= "Threate reviews API for Pune Rangmanch",
    lifespan=lifespan,
)


app.include_router(reviews_router)

@app.get("/")
def root():
    return {"Message": "Welcome to rangmanch review API"}
