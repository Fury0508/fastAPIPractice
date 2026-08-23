from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from routes.query import router as query_router

app = FastAPI(
    title="RAG_pipeline",
    description= "This is a RAG API",
    version = "0.1.0"
)

app.include_router(query_router)