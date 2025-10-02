from fastapi import FastAPI
from .routers import users, projects, milestones
from . import models, database

# Create tables if not exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="🚀 DevOps Tracker API")

@app.get("/")
def root():
    return {"message": "🚀 DevOps Tracker API is running!"}

# Register routers
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(milestones.router)
