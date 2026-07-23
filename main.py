from fastapi import FastAPI

from app.utils.exceptions import register_exception_handlers
from app.database.database import create_db_and_tables
from app.routes.suppliers import router as supplier_router
from app.routes.products import router as product_router

app = FastAPI(
    title="TechVault Inventory API",
    description="Inventory Management API for TechVault",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(supplier_router)
app.include_router(product_router)
register_exception_handlers(app)

@app.get("/")
def welcome():
    return {
        "message": "Welcome to the TechVault Inventory API",
        "status": "Running"
    }@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "message": "TechVault API is running"
    }