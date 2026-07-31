from traceback import StackSummary
from typing_extensions import deprecated
from fastapi import FastAPI
from fastapi import Request
import uvicorn
import asyncio

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

@app.get("/orders")
def list_orders():
    """List recent orders """
    return {
        "orders":[
            {"id":1,"item": "Butter Chicken", "status":"delivered"},
            {"id":2,"item": "Masala Dosa", "status":"preparing"},
            {"id":3,"item": "Paneer Tikka", "status":"delivered"},

        ]
    }

@app.get("/orders/status")
def order_status():
    """Get oder Status"""
    return {
        "total_today":2_340_23,
        "top_city": "Delhi"
    }


@app.get("/debug/request-info")
async def request_info(request: Request):
    """Inspect the raw request object"""
    return {
        "method":request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
    }


@app.get(
    "/orders/active",
    summary = "Get Active Orders",
    description = (
        "Return all orders that are currently beign prepared"
        "or are out for delivery"
    ),
    tags = ['orders'],
    response_description = "List of active order objects",
    deprecated = False
)
def get_active_order():
    """This docstring also appears in docs"""
    return {
        "active_orders": [
            {"id": 1, "item": "Masala Dosa","status":"out for delivery"}
        ]
    }

@app.get("/restaurants",tags = ['Restaurants'])
def list_restro():
    """another docs string for another endpoints"""
    return {
        "restaurants":[
            {"test":"test"}
        ]
    }

@app.get("/restaurants/delhi",tags = ['Restaurants',"delhi"])
def list_restro_delhi():
    """another docs string for another endpoints"""
    return {
        "restaurants":[
            {"test":"test"}
        ]
    }