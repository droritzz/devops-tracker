from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.routers import users, projects, milestones
from app import models, database
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wait for database to be ready and create tables
try:
    logger.info("Waiting for database to be ready...")
    database.wait_for_db()
    logger.info("Creating database tables...")
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    raise

# Initialize FastAPI app
app = FastAPI(title="🚀 DevOps Tracker API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "🚀 DevOps Tracker API is running!"}

# Favicon endpoint
@app.get("/favicon.ico")
async def favicon():
    # Return a simple 204 No Content response to avoid 404 errors
    from fastapi.responses import Response
    return Response(status_code=204)

# Register routers
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(milestones.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

