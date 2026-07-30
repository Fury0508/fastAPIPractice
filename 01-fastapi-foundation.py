from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title = "Swiggy Order Service",
    description= (
        "Internal API for managing orders"
        "It will handle creation, tracking of delivery system"
    ),
    version="1.2.1",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url= "/openapi.json"
)

@app.get("/")
def read_root():
    """Root endpoint - Health check """
    # FASTAPI converts this dict into JSON 
    return {"message": "Welcome to swiggy Order service",
    "status":"healthy"}

@app.get("/about")
def about():
    """ Returns API metadata"""
    return {
        "service":"order-service",
        "team":"backend platform",
        "region":"ap-south-1",
        "version":"1.2.2"
    }