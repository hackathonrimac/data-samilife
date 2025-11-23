import uvicorn
from fastapi import FastAPI
from app.routes import medical_routes
# from app.db.database import Base, engine

# Crear tablas al inicio (solo para dev)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Salud Rimac")

app.include_router(medical_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)