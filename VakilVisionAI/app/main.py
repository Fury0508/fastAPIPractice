from fastapi import FastAPI
from database import init_db
from routes.contracts import router as contracts_router
from routes.analysis import router as analysis_router
app = FastAPI(
    title="Vakeel Contract API",
    description= "Ai-Powered Contract Analysis using Gemini",
    version = "1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()  # Initialize the database and create indexes

@app.get("/")
async def root():
    return {
        "message": "Vakeel contracts API",
        "version": "1.0.0",
        "endpoints":{
            "Post /contracts/upload" : "Upload a pdf or text contract for analysis",
            "GET /contracts/": "Retrive a list of all uploaded contracts",
            "GET /contracts/{id}" : "Retrive details of a specific contract by ID",
            "POST /analysis/" : "Analyse a contract using aI and return insights",
            "GET /analysis/{analysis_id}" : "Retrieve the result of a specific analysis by Id",
            "GET /analysis/contract/{contract_id}" : "Retrieve a list of all analyses performed for a specific contract"
        }
    }

app.include_router(contracts_router)
app.include_router(analysis_router)