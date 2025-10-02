from fastapi import FastAPI
from . import models, database
from .routers import users, projects, milestones

# Create all tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="🚀 DevOps Tracker API")

# Root endpoint
@app.get("/")
def root():
    return {"message": "🚀 DevOps Tracker API is running!"}

# Register routers
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(milestones.router)
