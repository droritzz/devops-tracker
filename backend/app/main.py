from fastapi import FastAPI
from app.routers import users, projects, milestones
from app import models, database


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

